//+------------------------------------------------------------------+
//| BaoXtra BX42MR - MT5 Swing Semi-Auto v0.1 (REVIEW ONLY)           |
//| Adapted from Pine V4.2.8; this is a PARTIAL, independent port.   |
//| No OrderSend, no CTrade, no live or demo order placement.          |
//| D1 trend -> H4 FVG/OB proxy/Fib -> H1 -> M15 BOS + retest.       |
//+------------------------------------------------------------------+
#property strict
#property version "0.10"
#property description "BaoXtra BX42MR Swing REVIEW ONLY; no order execution"
#property description "M15 chart, D1-H4-H1 confirmed trend, zones, retest, Entry/SL/TP"

input group "01 | SAFE MODE"
input bool   InpEnableSignals      = true;
input bool   InpPopupAlert         = false;
input bool   InpPushToMobile       = false;   // requires MT5 desktop notification settings
input bool   InpShowLevelLines     = true;
input bool   InpShowH4Zones        = true;

input group "02 | Swing confirmation D1-H4-H1-M15"
input int    InpD1FastEMA         = 21;
input int    InpD1SlowEMA         = 50;
input int    InpH4FastEMA         = 21;
input int    InpH4SlowEMA         = 50;
input bool   InpH4TrendRequired   = true;
input int    InpH4ZoneMaxAge      = 30;
input int    InpH4TouchTTLM15     = 24;
input double InpH4FVGMinATR       = 0.15;
input double InpH4OBBodyATR       = 0.65;
input int    InpH4PivotLen       = 3;
input double InpFibFrom           = 0.382;
input double InpFibTo             = 0.618;
enum BX_H4_ZONE_MODE { BX_ANY_ZONE=0, BX_FVG_OR_OB=1, BX_TWO_ZONES=2 };
input BX_H4_ZONE_MODE InpZoneMode = BX_ANY_ZONE;
enum BX_H1_CONFIRM { BX_RSI_CANDLE=0, BX_RSI_EMA=1 };
input BX_H1_CONFIRM InpH1Confirm  = BX_RSI_CANDLE;
input double InpH1RSIBuyAbove    = 50.0;
input double InpH1RSISellBelow   = 50.0;
input int    InpH1FastEMA        = 21;
input int    InpH1SlowEMA        = 50;

input group "03 | M15 structure and retest"
input int    InpPivotLen          = 5;
input int    InpOBLookback        = 20;
input int    InpLockedTTL         = 10;
input int    InpM15FastEMA        = 21;
input int    InpM15SlowEMA        = 55;
input int    InpM15TrendEMA       = 200;
input double InpDisplacementATR   = 0.65;
input double InpMinBodyRatio      = 0.45;
input double InpCloseLocation     = 0.65;
input double InpMaxEntryATR       = 1.20;
input double InpMinLocalFVGATR    = 0.20;
input int    InpLocalFVGTTL       = 6;

input group "04 | Reference Entry SL TP / not broker orders"
input double InpSLBufferATR       = 0.30;
input double InpMinStopATR        = 0.80;
input double InpMaxStopATR        = 4.00;
input double InpMaxSpreadATR      = 0.25;
input double InpTP1R              = 1.00;
input double InpTP2R              = 2.00;
input double InpTP3R              = 3.00;
input double InpPreviewLot        = 0.01; // only for cost estimate, NEVER orders

struct BXZone
{
   bool     valid;
   double   lo;
   double   hi;
   datetime formed;
   string   label;
};
struct BXSetup
{
   int      side;
   datetime origin;
   double   invalid;
   BXZone   ob;
   BXZone   fvg;
   BXZone   fib;
};

int g_d1Fast=INVALID_HANDLE,g_d1Slow=INVALID_HANDLE;
int g_h4Fast=INVALID_HANDLE,g_h4Slow=INVALID_HANDLE,g_h4ATR=INVALID_HANDLE;
int g_h1Fast=INVALID_HANDLE,g_h1Slow=INVALID_HANDLE,g_h1RSI=INVALID_HANDLE;
int g_m15Fast=INVALID_HANDLE,g_m15Slow=INVALID_HANDLE,g_m15Trend=INVALID_HANDLE,g_m15ATR=INVALID_HANDLE;
BXSetup g_lock;
datetime g_lastBar=0,g_bearTouch=0,g_bullTouch=0;
string g_bearFingerprint="",g_bullFingerprint="";
string g_dashboard="Starting...";
const string BX_PREFIX="BX428_MT5_";

void BXClearZone(BXZone &z)
{
   z.valid=false;z.lo=0.0;z.hi=0.0;z.formed=0;z.label="";
}
void BXClearSetup()
{
   g_lock.side=0;g_lock.origin=0;g_lock.invalid=0.0;
   BXClearZone(g_lock.ob);BXClearZone(g_lock.fvg);BXClearZone(g_lock.fib);
}
void BXSetZone(BXZone &z,const double low,const double high,
               const datetime when,const string label)
{
   BXClearZone(z);
   if(low<=0.0 || high<=low) return;
   z.valid=true;z.lo=low;z.hi=high;z.formed=when;z.label=label;
}
bool BXBar(const ENUM_TIMEFRAMES tf,const int shift,MqlRates &b)
{
   MqlRates data[];
   if(CopyRates(_Symbol,tf,shift,1,data)!=1) return false;
   b=data[0];return b.time>0;
}
bool BXIndicator(const int handle,const int shift,double &v)
{
   v=0.0;
   if(handle==INVALID_HANDLE) return false;
   double tmp[];
   if(CopyBuffer(handle,0,shift,1,tmp)!=1) return false;
   if(tmp[0]==EMPTY_VALUE || !MathIsValidNumber(tmp[0]))return false;
   v=tmp[0];return true;
}
int BXHandleMA(const ENUM_TIMEFRAMES tf,const int length)
{
   return iMA(_Symbol,tf,length,0,MODE_EMA,PRICE_CLOSE);
}
bool BXValidInputs()
{
   return (InpD1FastEMA>0 && InpD1FastEMA<InpD1SlowEMA &&
       InpH4FastEMA>0 && InpH4FastEMA<InpH4SlowEMA &&
       InpH1FastEMA>0 && InpH1FastEMA<InpH1SlowEMA &&
       InpPivotLen>=2 && InpOBLookback>=2 && InpH4ZoneMaxAge>=3 &&
       InpH4TouchTTLM15>=1 && InpLockedTTL>=2 && InpH4PivotLen>=2 &&
       InpFibFrom>=0.0 && InpFibFrom<InpFibTo && InpFibTo<=1.0 &&
       InpTP1R>0.0 && InpTP2R>InpTP1R && InpTP3R>InpTP2R &&
       InpMinStopATR>0.0 && InpMaxStopATR>InpMinStopATR &&
       InpH1RSIBuyAbove>=0.0 && InpH1RSIBuyAbove<=100.0 &&
       InpH1RSISellBelow>=0.0 && InpH1RSISellBelow<=100.0 &&
       InpPreviewLot>0.0 && InpMaxSpreadATR>0.0);
}
int OnInit()
{
   if(!BXValidInputs()){Print("BX42: invalid inputs. EA not initialized.");return INIT_PARAMETERS_INCORRECT;}
   g_d1Fast=BXHandleMA(PERIOD_D1,InpD1FastEMA);
   g_d1Slow=BXHandleMA(PERIOD_D1,InpD1SlowEMA);
   g_h4Fast=BXHandleMA(PERIOD_H4,InpH4FastEMA);
   g_h4Slow=BXHandleMA(PERIOD_H4,InpH4SlowEMA);
   g_h4ATR=iATR(_Symbol,PERIOD_H4,14);
   g_h1Fast=BXHandleMA(PERIOD_H1,InpH1FastEMA);
   g_h1Slow=BXHandleMA(PERIOD_H1,InpH1SlowEMA);
   g_h1RSI=iRSI(_Symbol,PERIOD_H1,14,PRICE_CLOSE);
   g_m15Fast=BXHandleMA(PERIOD_M15,InpM15FastEMA);
   g_m15Slow=BXHandleMA(PERIOD_M15,InpM15SlowEMA);
   g_m15Trend=BXHandleMA(PERIOD_M15,InpM15TrendEMA);
   g_m15ATR=iATR(_Symbol,PERIOD_M15,14);
   if(g_d1Fast==INVALID_HANDLE || g_d1Slow==INVALID_HANDLE ||
      g_h4Fast==INVALID_HANDLE || g_h4Slow==INVALID_HANDLE ||
      g_h4ATR==INVALID_HANDLE || g_h1Fast==INVALID_HANDLE ||
      g_h1Slow==INVALID_HANDLE || g_h1RSI==INVALID_HANDLE ||
      g_m15Fast==INVALID_HANDLE || g_m15Slow==INVALID_HANDLE ||
      g_m15Trend==INVALID_HANDLE || g_m15ATR==INVALID_HANDLE)
   {Print("BX42: indicator creation failed: ",GetLastError());return INIT_FAILED;}
   BXClearSetup();g_lastBar=iTime(_Symbol,PERIOD_M15,0);
   Print("BX42 MR MT5 v0.1: REVIEW_ONLY, M15, no broker orders (demo/manual study).");
   return INIT_SUCCEEDED;
}
void BXRelease(const int handle){if(handle!=INVALID_HANDLE)IndicatorRelease(handle);}
void BXDeleteLevel(const string name){ObjectDelete(0,BX_PREFIX+name);}
void OnDeinit(const int reason)
{
   BXRelease(g_d1Fast);BXRelease(g_d1Slow);BXRelease(g_h4Fast);
   BXRelease(g_h4Slow);BXRelease(g_h4ATR);BXRelease(g_h1Fast);
   BXRelease(g_h1Slow);BXRelease(g_h1RSI);BXRelease(g_m15Fast);
   BXRelease(g_m15Slow);BXRelease(g_m15Trend);BXRelease(g_m15ATR);
   BXDeleteLevel("ENTRY");BXDeleteLevel("SL");BXDeleteLevel("TP1");
   BXDeleteLevel("TP2");BXDeleteLevel("TP3");
   BXDeleteLevel("H4_SUPPLY_HI");BXDeleteLevel("H4_SUPPLY_LO");
   BXDeleteLevel("H4_DEMAND_HI");BXDeleteLevel("H4_DEMAND_LO");
   Comment("");
}

// Confirmed pivots: a pivot at shift >= right+1 can only use closed candles.
bool BXFindPivot(const ENUM_TIMEFRAMES tf,const bool highPivot,
                 const int right,const int maxLookback,double &price,int &index)
{
   price=0.0;index=-1;
   for(int sh=right+1;sh<=maxLookback;sh++)
   {
      MqlRates mid;
      if(!BXBar(tf,sh,mid))return false;
      double p=highPivot?mid.high:mid.low;
      bool isPivot=true;
      for(int k=1;k<=right;k++)
      {
         MqlRates newer,older;
         if(!BXBar(tf,sh-k,newer) || !BXBar(tf,sh+k,older))return false;
         if(highPivot ? (newer.high>=p || older.high>=p)
                      : (newer.low<=p || older.low<=p)){isPivot=false;break;}
      }
      if(isPivot){price=p;index=sh;return true;}
   }
   return false;
}
bool BXH4Zone(const int side,const bool fvg,const int maxAge,BXZone &z)
{
   BXClearZone(z);
   for(int sh=1;sh<=maxAge;sh++)
   {
      MqlRates b,old;
      double atr;
      if(!BXBar(PERIOD_H4,sh,b)||!BXBar(PERIOD_H4,sh+2,old)||
         !BXIndicator(g_h4ATR,sh,atr))return false;
      double lo=0.0,hi=0.0;
      if(fvg)
      {
         if(side<0 && b.high<old.low && old.low-b.high>=atr*InpH4FVGMinATR)
            {lo=b.high;hi=old.low;}
         if(side>0 && b.low>old.high && b.low-old.high>=atr*InpH4FVGMinATR)
            {lo=old.high;hi=b.low;}
      }
      else
      {
         MqlRates prev;
         if(!BXBar(PERIOD_H4,sh+1,prev))return false;
         if(side<0 && b.close<b.open && prev.close>prev.open &&
            b.open-b.close>=atr*InpH4OBBodyATR){lo=prev.low;hi=prev.high;}
         if(side>0 && b.close>b.open && prev.close<prev.open &&
            b.close-b.open>=atr*InpH4OBBodyATR){lo=prev.low;hi=prev.high;}
      }
      if(hi>lo)
      {
         BXSetZone(z,lo,hi,b.time,fvg?"H4 FVG":"H4 OB proxy");
         return z.valid;
      }
   }
   return false;
}
bool BXH4Fib(const int side,BXZone &z)
{
   BXClearZone(z);
   double ph,pl;int highShift,lowShift;
   if(!BXFindPivot(PERIOD_H4,true,InpH4PivotLen,110,ph,highShift) ||
      !BXFindPivot(PERIOD_H4,false,InpH4PivotLen,110,pl,lowShift) || ph<=pl)return false;
   double span=ph-pl,lo=0.0,hi=0.0;
   if(side<0 && lowShift<highShift)
   {lo=pl+span*InpFibFrom;hi=pl+span*InpFibTo;}
   else if(side>0 && highShift<lowShift)
   {lo=ph-span*InpFibTo;hi=ph-span*InpFibFrom;}
   else return false;
   MqlRates b;if(!BXBar(PERIOD_H4,1,b))return false;
   BXSetZone(z,lo,hi,b.time,"H4 Fib");return z.valid;
}
bool BXInside(const BXZone &z,const MqlRates &c)
{
   return z.valid && c.low<=z.hi && c.high>=z.lo;
}
bool BXH4Active(const int side,const BXZone &z,const MqlRates &h4)
{
   if(!z.valid)return false;
   return side>0 ? h4.close>=z.lo : h4.close<=z.hi;
}
string BXZoneKey(const BXZone &fvg,const BXZone &ob,const BXZone &fib)
{
   return DoubleToString(fvg.lo,_Digits)+"/"+DoubleToString(fvg.hi,_Digits)+";"+
          DoubleToString(ob.lo,_Digits)+"/"+DoubleToString(ob.hi,_Digits)+";"+
          DoubleToString(fib.lo,_Digits)+"/"+DoubleToString(fib.hi,_Digits);
}
bool BXH1Confirm(const int side,string &reason)
{
   MqlRates h;
   double rsi,fast,slow;
   if(!BXBar(PERIOD_H1,1,h)||!BXIndicator(g_h1RSI,1,rsi)||
      !BXIndicator(g_h1Fast,1,fast)||!BXIndicator(g_h1Slow,1,slow))
   {reason="H1 DATA MISSING";return false;}
   bool okRSI=(side>0?rsi>InpH1RSIBuyAbove:rsi<InpH1RSISellBelow);
   bool okExtra=false;
   if(InpH1Confirm==BX_RSI_CANDLE)okExtra=side>0?(h.close>h.open):(h.close<h.open);
   else okExtra=side>0?(h.close>fast && fast>slow):(h.close<fast && fast<slow);
   reason=StringFormat("H1 RSI %.1f %s",rsi,okRSI&&okExtra?"OK":"WAIT");
   return okRSI&&okExtra;
}
bool BXCandleConfirm(const int side,const MqlRates &b)
{
   double range=MathMax(b.high-b.low,_Point);
   double body=MathAbs(b.close-b.open);
   if(body/range<InpMinBodyRatio)return false;
   if(side>0)return b.close>b.open && (b.close-b.low)/range>=InpCloseLocation;
   return b.close<b.open && (b.high-b.close)/range>=InpCloseLocation;
}
void BXLocalZone(const int side,const bool fvg,const MqlRates &latest,const double atr,BXZone &z)
{
   BXClearZone(z);
   for(int sh=2;sh<=(fvg?InpLocalFVGTTL+1:InpOBLookback+1);sh++)
   {
      MqlRates b;
      if(!BXBar(PERIOD_M15,sh,b))return;
      if(!fvg)
      {
         if((side>0&&b.close<b.open)||(side<0&&b.close>b.open))
         {BXSetZone(z,b.low,b.high,b.time,"M15 OB proxy");return;}
      }
      else
      {
         MqlRates older;
         if(!BXBar(PERIOD_M15,sh+2,older))return;
         if(side>0 && b.low>older.high && b.low-older.high>=atr*InpMinLocalFVGATR)
         {BXSetZone(z,older.high,b.low,b.time,"M15 FVG");return;}
         if(side<0 && b.high<older.low && older.low-b.high>=atr*InpMinLocalFVGATR)
         {BXSetZone(z,b.high,older.low,b.time,"M15 FVG");return;}
      }
   }
}
void BXLockStructure(const int side,const MqlRates &latest,const double atr,
                     const double recentLow,const double recentHigh)
{
   BXClearSetup();g_lock.side=side;g_lock.origin=latest.time;
   BXLocalZone(side,false,latest,atr,g_lock.ob);
   BXLocalZone(side,true,latest,atr,g_lock.fvg);
   double extent=side>0?latest.high-recentLow:recentHigh-latest.low;
   if(extent>2.0*atr)
   {
      double lo,hi;
      if(side>0){lo=latest.high-extent*InpFibTo;hi=latest.high-extent*InpFibFrom;}
      else {lo=latest.low+extent*InpFibFrom;hi=latest.low+extent*InpFibTo;}
      BXSetZone(g_lock.fib,lo,hi,latest.time,"M15 Fib");
   }
   double reference=side>0?MathMin(latest.low,recentLow):MathMax(latest.high,recentHigh);
   g_lock.invalid=reference-side*atr*InpSLBufferATR;
   if(!g_lock.ob.valid && !g_lock.fvg.valid && !g_lock.fib.valid)BXClearSetup();
}
int BXAgeM15(const datetime since)
{
   if(since<=0)return 999999;
   int shift=iBarShift(_Symbol,PERIOD_M15,since,true);
   return shift<0 ? 999999 : shift-1; // just-closed candle has shift 1 => age 0
}
void BXLine(const string key,const double price,const color clr)
{
   const string name=BX_PREFIX+key;
   if(ObjectFind(0,name)<0)ObjectCreate(0,name,OBJ_HLINE,0,0,price);
   ObjectSetDouble(0,name,OBJPROP_PRICE,price);
   ObjectSetInteger(0,name,OBJPROP_COLOR,clr);
   ObjectSetInteger(0,name,OBJPROP_WIDTH,2);
   ObjectSetString(0,name,OBJPROP_TEXT,key+" "+DoubleToString(price,_Digits));
}
void BXDrawPlan(const int side,const double entry,const double sl,
                const double tp1,const double tp2,const double tp3)
{
   if(!InpShowLevelLines)return;
   BXLine("ENTRY",entry,clrGold);BXLine("SL",sl,clrTomato);
   BXLine("TP1",tp1,clrLimeGreen);BXLine("TP2",tp2,clrSeaGreen);
   BXLine("TP3",tp3,clrDodgerBlue);
}
void BXNotify(const string message)
{
   Print(message);
   if(InpPopupAlert)Alert(message);
   if(InpPushToMobile && !MQLInfoInteger(MQL_TESTER))
   {
      if(!SendNotification(message))Print("BX42: push failed, check MetaQuotes ID and terminal settings");
   }
}
void BXNewClosedM15()
{
   MqlRates bar,daily,h4;
   double atr,df,ds,hf,hs,emaFast,emaSlow,emaTrend;
   if(!BXBar(PERIOD_M15,1,bar)||!BXBar(PERIOD_D1,1,daily)||
      !BXBar(PERIOD_H4,1,h4)||!BXIndicator(g_m15ATR,1,atr)||
      !BXIndicator(g_d1Fast,1,df)||!BXIndicator(g_d1Slow,1,ds)||
      !BXIndicator(g_h4Fast,1,hf)||!BXIndicator(g_h4Slow,1,hs)||
      !BXIndicator(g_m15Fast,1,emaFast)||!BXIndicator(g_m15Slow,1,emaSlow)||
      !BXIndicator(g_m15Trend,1,emaTrend) || atr<=0)
   {g_dashboard="WAIT: closed-bar history or indicators unavailable";return;}
   int d1Dir=0,h4Dir=0;
   if(daily.close>ds && df>ds)d1Dir=1;
   if(daily.close<ds && df<ds)d1Dir=-1;
   if(h4.close>hs && hf>hs)h4Dir=1;
   if(h4.close<hs && hf<hs)h4Dir=-1;
   BXZone bFvg,bOb,bFib,uFvg,uOb,uFib;
   BXH4Zone(-1,true,InpH4ZoneMaxAge,bFvg);
   BXH4Zone(-1,false,InpH4ZoneMaxAge,bOb);
   BXH4Fib(-1,bFib);
   BXH4Zone(1,true,InpH4ZoneMaxAge,uFvg);
   BXH4Zone(1,false,InpH4ZoneMaxAge,uOb);
   BXH4Fib(1,uFib);
   string sellKey=BXZoneKey(bFvg,bOb,bFib),buyKey=BXZoneKey(uFvg,uOb,uFib);
   if(sellKey!=g_bearFingerprint){g_bearFingerprint=sellKey;g_bearTouch=0;}
   if(buyKey!=g_bullFingerprint){g_bullFingerprint=buyKey;g_bullTouch=0;}
   bool sf=BXH4Active(-1,bFvg,h4)&&BXInside(bFvg,bar);
   bool so=BXH4Active(-1,bOb,h4)&&BXInside(bOb,bar);
   bool si=BXH4Active(-1,bFib,h4)&&BXInside(bFib,bar);
   bool uf=BXH4Active(1,uFvg,h4)&&BXInside(uFvg,bar);
   bool uo=BXH4Active(1,uOb,h4)&&BXInside(uOb,bar);
   bool ui=BXH4Active(1,uFib,h4)&&BXInside(uFib,bar);
   int sellHits=(sf?1:0)+(so?1:0)+(si?1:0);
   int buyHits=(uf?1:0)+(uo?1:0)+(ui?1:0);
   bool sellTouched=(InpZoneMode==BX_TWO_ZONES?sellHits>=2:
                    InpZoneMode==BX_FVG_OR_OB?sf||so:sellHits>0);
   bool buyTouched=(InpZoneMode==BX_TWO_ZONES?buyHits>=2:
                   InpZoneMode==BX_FVG_OR_OB?uf||uo:buyHits>0);
   if(sellTouched)g_bearTouch=bar.time;
   if(buyTouched)g_bullTouch=bar.time;
   bool sellRecent=BXAgeM15(g_bearTouch)<=InpH4TouchTTLM15;
   bool buyRecent=BXAgeM15(g_bullTouch)<=InpH4TouchTTLM15;
   if(InpShowH4Zones)
   {
      BXZone sup,dem;BXClearZone(sup);BXClearZone(dem);
      if(bFvg.valid)sup=bFvg;else if(bOb.valid)sup=bOb;else if(bFib.valid)sup=bFib;
      if(uFvg.valid)dem=uFvg;else if(uOb.valid)dem=uOb;else if(uFib.valid)dem=uFib;
      if(sup.valid){BXLine("H4_SUPPLY_HI",sup.hi,clrTomato);
                     BXLine("H4_SUPPLY_LO",sup.lo,clrTomato);}
      if(dem.valid){BXLine("H4_DEMAND_HI",dem.hi,clrDeepSkyBlue);
                     BXLine("H4_DEMAND_LO",dem.lo,clrDeepSkyBlue);}
   }
   // Setup only after confirmed M15 swing BOS with displacement.
   double highPivot,lowPivot;int hiIdx,loIdx;
   bool hasHi=BXFindPivot(PERIOD_M15,true,InpPivotLen,125,highPivot,hiIdx);
   bool hasLo=BXFindPivot(PERIOD_M15,false,InpPivotLen,125,lowPivot,loIdx);
   MqlRates prev;
   if(!BXBar(PERIOD_M15,2,prev)||!hasHi||!hasLo)
   {g_dashboard="WAIT: M15 confirmed swing pivots unavailable";return;}
   double range=MathMax(bar.high-bar.low,_Point),body=MathAbs(bar.close-bar.open);
   bool bullDisp=bar.close>bar.open && body>=atr*InpDisplacementATR &&
                 (bar.close-bar.low)/range>=InpCloseLocation;
   bool bearDisp=bar.close<bar.open && body>=atr*InpDisplacementATR &&
                 (bar.high-bar.close)/range>=InpCloseLocation;
   bool bullBreak=bullDisp && bar.close>highPivot && prev.close<=highPivot;
   bool bearBreak=bearDisp && bar.close<lowPivot && prev.close>=lowPivot;
   if(g_lock.side!=0 &&
      (BXAgeM15(g_lock.origin)>InpLockedTTL ||
       (g_lock.side>0 && bar.close<g_lock.invalid) ||
       (g_lock.side<0 && bar.close>g_lock.invalid) ||
       (g_lock.side>0 && bearBreak) || (g_lock.side<0 && bullBreak)))BXClearSetup();
   // A locked signal must retest on a *later* closed M15 bar.
   int ready=0;double entry=0,sl=0,tp1=0,tp2=0,tp3=0;
   string h1Reason="";
   if(g_lock.side!=0 && bar.time>g_lock.origin)
   {
      int side=g_lock.side;
      BXZone selected;BXClearZone(selected);
      if(BXInside(g_lock.ob,bar))selected=g_lock.ob;
      else if(BXInside(g_lock.fvg,bar))selected=g_lock.fvg;
      else if(BXInside(g_lock.fib,bar))selected=g_lock.fib;
      bool retest=selected.valid && BXCandleConfirm(side,bar) &&
         (side>0?bar.close>selected.lo:bar.close<selected.hi) &&
         (side>0?bar.close-selected.hi<=atr*InpMaxEntryATR:
                 selected.lo-bar.close<=atr*InpMaxEntryATR);
      bool trend=(side==d1Dir) && (!InpH4TrendRequired||h4Dir==side);
      bool zone=(side>0?buyRecent:sellRecent);
      bool h1=BXH1Confirm(side,h1Reason);
      bool ema=(side>0?emaFast>emaSlow && bar.close>emaTrend:
                         emaFast<emaSlow && bar.close<emaTrend);
      MqlTick tick;
      bool tickOK=SymbolInfoTick(_Symbol,tick) && tick.ask>0 && tick.bid>0;
      double spread=tickOK?tick.ask-tick.bid:1e10;
      bool spreadOK=spread<=atr*InpMaxSpreadATR;
      if(retest && trend && zone && h1 && ema && spreadOK)
      {
         entry=bar.close;double structural=side>0?MathMin(bar.low,selected.lo):
                                            MathMax(bar.high,selected.hi);
         double rawStop=structural-side*atr*InpSLBufferATR;
         double distance=MathMax(MathAbs(entry-rawStop),atr*InpMinStopATR);
         sl=entry-side*distance;
         if(distance<=atr*InpMaxStopATR && distance>2.0*spread && sl>0.0)
         {
            const double tickSize=SymbolInfoDouble(_Symbol,SYMBOL_TRADE_TICK_SIZE);
            if(tickSize>0.0)
            {
               entry=NormalizeDouble(MathRound(entry/tickSize)*tickSize,_Digits);
               sl=NormalizeDouble((side>0?MathFloor(sl/tickSize):MathCeil(sl/tickSize))*tickSize,_Digits);
            }
            distance=MathAbs(entry-sl);
            tp1=NormalizeDouble(entry+side*distance*InpTP1R,_Digits);
            tp2=NormalizeDouble(entry+side*distance*InpTP2R,_Digits);
            tp3=NormalizeDouble(entry+side*distance*InpTP3R,_Digits);
            ready=side;BXClearSetup();
         }
      }
   }
   // No new lock on the same bar that produces a completed plan.
   if(ready==0 && g_lock.side==0 && InpEnableSignals)
   {
      if(bullBreak && d1Dir==1)BXLockStructure(1,bar,atr,lowPivot,highPivot);
      else if(bearBreak && d1Dir==-1)BXLockStructure(-1,bar,atr,lowPivot,highPivot);
   }
   g_dashboard=StringFormat("BX42MR MT5 v0.1 | REVIEW ONLY | %s M15\n",_Symbol);
   g_dashboard+=StringFormat("D1: %s | H4 EMA: %s | H4 touch SELL:%s BUY:%s\n",
                d1Dir>0?"BUY":d1Dir<0?"SELL":"SIDEWAYS",
                h4Dir>0?"BUY":h4Dir<0?"SELL":"SIDEWAYS",
                sellRecent?"YES":"NO",buyRecent?"YES":"NO");
   g_dashboard+=StringFormat("Setup: %s | %s | ATR: %s\n",
                g_lock.side>0?"LOCK BUY":g_lock.side<0?"LOCK SELL":"WAIT",
                h1Reason,DoubleToString(atr,_Digits));
   if(ready!=0)
   {
      BXDrawPlan(ready,entry,sl,tp1,tp2,tp3);
      string msg=StringFormat("BX42 %s %s M15 REVIEW ENTRY=%s SL=%s TP1=%s TP2=%s TP3=%s",
         _Symbol,ready>0?"BUY":"SELL",DoubleToString(entry,_Digits),
         DoubleToString(sl,_Digits),DoubleToString(tp1,_Digits),
         DoubleToString(tp2,_Digits),DoubleToString(tp3,_Digits));
      g_dashboard+=msg+"\nMANUAL REVIEW / NOT A MARKET ORDER";
      BXNotify(msg);
   }
   else g_dashboard+="WAIT CONFLUENCE: no new manual plan; prior level lines may be historical.";
}
void OnTick()
{
   if(_Period!=PERIOD_M15)
   {Comment("BX42MR: USE M15 chart. REVIEW ONLY; no orders.");return;}
   if(!InpEnableSignals){Comment("BX42MR: PAUSED. REVIEW ONLY.");return;}
   datetime openTime=iTime(_Symbol,PERIOD_M15,0);
   if(openTime<=0){Comment("BX42MR: WAIT FOR M15 DATA");return;}
   if(g_lastBar==0){g_lastBar=openTime;return;}
   if(openTime!=g_lastBar){g_lastBar=openTime;BXNewClosedM15();}
   Comment(g_dashboard);
}
