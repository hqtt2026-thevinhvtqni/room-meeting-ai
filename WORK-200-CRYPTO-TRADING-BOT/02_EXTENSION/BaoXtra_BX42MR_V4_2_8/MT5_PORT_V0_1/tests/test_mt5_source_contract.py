"""Static checks only; not a MetaEditor compile or TradingView parity test."""
import pathlib, re

SRC = pathlib.Path(__file__).resolve().parents[1].joinpath("BaoXtra_BX42MR_MT5_Swing_SemiAuto_v0_1.mq5").read_text()


def test_contains_required_callbacks_and_swing_parts():
    for name in ("OnInit", "OnTick", "OnDeinit", "BXNewClosedM15", "BXLockStructure", "BXH4Zone", "BXH4Fib", "BXH1Confirm", "BXCandleConfirm", "BXDrawPlan"):
        assert re.search(r"\b"+name+r"\s*\(", SRC)


def test_no_broker_order_execution_calls():
    stripped = re.sub(r"//[^\n]*", "", SRC)
    for pattern in (r"\bOrderSend\s*\(", r"\bOrderSendAsync\s*\(",r"\bCTrade\b",r"\btrade\.Buy\s*\(",r"\btrade\.Sell\s*\(",r"\bPositionOpen\s*\("):
        assert not re.search(pattern, stripped), pattern


def test_closed_higher_timeframe_only():
    # All HTF indicators and price bars must be read from shift 1 or greater.
    for tf in ("PERIOD_H4", "PERIOD_H1", "PERIOD_D1"):
        assert f"BXBar({tf},1" in SRC
    assert "BXIndicator(g_h1RSI,1" in SRC
    assert "BXIndicator(g_d1Fast,1" in SRC
    assert "BXIndicator(g_h4Fast,1" in SRC
    assert not re.search(r"BXBar\(PERIOD_(D1|H4|H1),0", SRC)


def test_m15_chart_gated_and_lock_then_retest():
    assert "_Period!=PERIOD_M15" in SRC
    assert "bar.time>g_lock.origin" in SRC
    assert "BXAgeM15(g_lock.origin)>InpLockedTTL" in SRC


def test_demo_defaults_and_manual_only():
    assert "InpPushToMobile       = false" in SRC
    assert "InpPopupAlert         = false" in SRC
    assert "InpPreviewLot        = 0.01" in SRC
    assert "REVIEW ONLY" in SRC


def test_swing_config_contains_risk_targets():
    for v in ("InpFibFrom", "InpFibTo", "InpTP1R", "InpTP2R", "InpTP3R", "InpSLBufferATR", "InpMaxSpreadATR", "InpH4TouchTTLM15"):
        assert v in SRC


def test_balanced_brackets_naive_removed_comments_and_strings():
    no_comments = re.sub(r"//[^\n]*", "", SRC)
    clean=re.sub(r'"(?:\\.|[^"\\])*"', '""', no_comments)
    stack=[]
    matches={'}':'{',')':'(',']':'['}
    for c in clean:
        if c in '{([': stack.append(c)
        elif c in '})]':
            assert stack and stack.pop()==matches[c]
    assert not stack
