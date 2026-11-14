# W116 SOURCE CATALOG — FIRST SOURCE

## SRC-001 — public-apis/public-apis
- Type: DISCOVERY_DIRECTORY
- Canonical URL: https://github.com/public-apis/public-apis
- Default branch inspected: master
- Visibility: Public
- Archived: No (repository metadata at inspection)
- Repository license: MIT (LICENSE file read from master)
- README finding: The repository describes itself as a manually curated public API list and currently includes both API entries and a section named MCP Servers.
- Useful for ROOM-HOP: Discover candidate APIs and Agent-callable MCP servers by category; compare the metadata exposed by the directory; identify provider documentation and installation links.
- Not useful for: Directly executing an API call, proving a provider is live, proving that an API is free, or granting an Agent permission.
- Practical assessment: PASS as a source directory; NOT AN EXECUTABLE SERVICE.
- Runtime test: NOT APPLICABLE to the repository itself. Individual entries are NOT TESTED until separately inspected/called in an authorized test.
- Important caveat: MIT applies to the repository's own content. It does not replace each API provider's terms, license, pricing, authentication, privacy policy or usage limits.
- Source freshness: Check the upstream README and provider docs when selecting a specific entry; do not assume the catalog entry is current.

## Selection rule
Prioritize tools that solve an identified ROOM-HOP need. For each selected entry, create one concise resource record with its own source URL, purpose, protocol/endpoint, authentication, cost/quota, privacy/security notes, compatibility, test evidence and status.


# FINANCE & INVESTMENT RESOURCES — INITIAL EXPANSION

## Financial classification
- RES-03 Finance & Investment: issuer research, statements, portfolio analytics, valuation, quant research.
- RES-04 Market Data: prices, OHLCV, order books, indices, corporate actions and crypto market data.
- RES-05 Banking & Economy: central-bank series, rates, FX, inflation, GDP and macroeconomic indicators.

## FIN-001 — SSI FastConnect API
Official Vietnamese broker API documentation describes REST market data for HOSE/HNX/UPCOM, daily trading data, OHLCV intervals, indices, corporate actions and WebSocket streams. It also documents order placement/amend/cancel, account and portfolio access. Classified as CANDIDATE: official documentation reviewed; no credentials or runtime calls used. Market-data read scope must be separated from trading scopes.
Source: https://developers.ssi.com.vn/docs/getting-started/overview

## FIN-002 — FRED API
Official St. Louis Fed API for FRED/ALFRED economic time series, observations, releases and historical vintages. API key required. Documentation reviewed; runtime not tested.
Source: https://fred.stlouisfed.org/docs/api/fred/

## FIN-003 — SEC EDGAR APIs
Official SEC public submissions and XBRL company facts/filings data. Public API access uses a declared User-Agent and fair-access requirements. Documentation reference recorded; runtime not tested.
Source: https://www.sec.gov/edgar/sec-api-documentation

## FIN-004 — CCXT
Mature open-source multi-exchange library. Public market data can be accessed without exchange keys on supported venues; private API methods can read accounts and execute trades/transfers. Catalog as CANDIDATE for read-only market-data integration; private methods remain out of scope. Documentation/repository reviewed; runtime not tested.
Sources: https://github.com/ccxt/ccxt and https://github.com/ccxt/ccxt/wiki/Manual

## FIN-005 — fin-data-mcp
Community MCP project aggregates several finance data providers. GitHub snapshot showed a very small project (4 stars, 1 commit); record as LOW-MATURITY CANDIDATE only. Requires code/dependency/security review and runtime tests before installation.
Source: https://github.com/CohenD/fin-data-mcp

## FIN-006 — awesome-finance-mcp
Curated discovery directory for finance MCP servers. It is a directory, not an executable MCP service. Each listed server requires independent source, license, maintenance, security and runtime review.
Source: https://github.com/BlockRunAI/awesome-finance-mcp

## FIN-007 — Frankfurter API
Reference exchange-rate API based on central-bank data including ECB reference rates. Useful for historical/reference FX, not a live executable quote. Documentation reference recorded; runtime not tested.
Source: https://frankfurter.dev/

## FIN-008 — World Bank Indicators API
Official public API for development and macro indicators across countries. Useful for long-horizon macro context; verify indicator definition, unit, frequency and release lag. Runtime not tested.
Source: https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information

## Important status distinction
These additions are documented candidates, not runtime PASS. Only the upstream documentation/repository was reviewed. No broker account, API key, trade endpoint or external MCP server was connected or executed.


# PUBLIC ADMINISTRATION, PUBLIC INVESTMENT, CONSTRUCTION, HEALTH, EDUCATION & I CHING

## RES-13 / RES-14 — Public administration and legal sources
### GOV-001 — National Public Service Portal
Official portal supports lookup of administrative procedures and online public services, identifies responsible agencies, and supports tracking hồ sơ by reference number. Public lookup is useful; authenticated submission is a separate high-risk workflow. No public API contract verified.
- Source: https://vpcp.dichvucong.gov.vn/p/home/dvc-gioi-thieu.html
- Status: CANDIDATE / portal reviewed / runtime not tested.

### GOV-002 — National Legal Documents Database (vbpl.vn)
Official legal-document source with full text, attributes, validity status, history, related documents and downloadable files. Useful for grounded legal retrieval; no public API contract verified.
- Source: https://vbpl.vn/
- Status: CANDIDATE / official portal reviewed / runtime not tested.

## RES-15 / RES-16 — Public investment and procurement
### PUB-001 — National Public Investment Information System
The Ministry portal lists a national public investment information system/database. Existence and institutional role are confirmed; open API/public bulk access are NOT confirmed.
- Discovery source: https://www.mpi.gov.vn/portal/Pages/default.aspx
- Status: CANDIDATE / access model unverified.

### PUB-002 — Vietnam National E-Procurement System (VNEPS)
Official portal provides search for bidding notices, contractor/investor selection, procurement plans and project information. Public web search is visible; public API not verified.
- Source: https://muasamcong.mof.gov.vn/en/web/guest/business/ebidding
- Status: CANDIDATE / portal reviewed / runtime not tested.

## RES-17 / RES-18 — Construction
### CON-001 — National Construction Activity Database
Official construction information system reference at https://csdlhdxd.gov.vn/. Public API, access level and export capability still need confirmation.
- Status: CANDIDATE / access unverified.

### CON-002 — CEMIA construction norms, prices and indices
Officially referenced information system for construction norms, prices, direct cost elements and construction price indices at https://cemia.gov.vn/. Public API/export access still needs confirmation.
- Status: CANDIDATE / access unverified.

## RES-19 / RES-20 — Health
### HLT-001 — NSO Vietnam health statistics
Official tables include health facilities, beds, doctors and medical staff, with statistical indicators. Aggregate statistics only; not clinical records.
- Source: https://www.nso.gov.vn/so-lieu-thong-ke/
- Status: CANDIDATE / official statistics reviewed / runtime not tested.

## RES-21 — Education
### EDU-001 — NSO Vietnam education statistics
Official indicator system includes schools, classes, classrooms, teachers, pupils and enrollment/access measures.
- Source: https://www.nso.gov.vn/phuong-phap-luan-thong-ke/he-thong-chi-tieu-thong-ke/
- Status: CANDIDATE / official statistics reviewed / runtime not tested.

## RES-22 / RES-23 — I Ching and classical texts
### ICH-001 — 64 hexagrams of the I Ching (Nhật Nguyệt)
Vietnamese structured dataset of 64 hexagrams with Vietnamese/Han names and trigram structure; CSV/Hugging Face distribution, CC BY 4.0 attribution stated by publisher. This is a structured reference table, not a complete classical-text/commentary corpus.
- Source: https://nhatnguyet.org/en/du-lieu
- Dataset: https://huggingface.co/datasets/nhatnguyet/64-que-kinh-dich
- Status: CANDIDATE / metadata reviewed / runtime not tested.

## Agent use rule for regulated/public domains
Use official primary sources first. Treat portal existence as distinct from callable API access. Do not submit public-service applications, bids, signatures, payments, or change government records. Health resources here are aggregate statistics, not personal medical records. For legal answers preserve the exact document, status, effective date and amendment history. For I Ching, keep source text and commentary distinct from modern interpretation or AI-generated readings.


# RES-24 — VIETNAM LAW & LEGAL RESEARCH

A dedicated legal-resource category for ROOM-HOP Agents. Prefer official primary sources and preserve document identity, validity, effective date, amendment chain and original publication. A searchable portal is not automatically a public API.

## LAW-001 — Cổng Pháp luật Quốc gia
Ministry of Justice-managed national portal with legal document search, new instruments, draft legislation, legal support and policy feedback entry points.
- Portal: https://phapluat.gov.vn/
- Legal documents: https://phapluat.gov.vn/he-thong-van-ban-phap-luat
- Status: Official portal reviewed; API/runtime not tested. [Source](https://phapluat.gov.vn/he-thong-van-ban-phap-luat)

## LAW-002 — Cơ sở dữ liệu quốc gia về văn bản pháp luật (VBPL)
Ministry of Justice database for central and local legal normative documents, consolidated texts and legal document search. The Ministry's guide describes the database coverage and search functions.
- Portal: https://vbpl.moj.gov.vn/pages/portal.aspx
- User guide: https://vbpl.moj.gov.vn/huongdan/csdlvbplquocgia.htm
- Status: Official database and guide reviewed; API/runtime not tested. [Sources](https://vbpl.moj.gov.vn/huongdan/csdlvbplquocgia.htm) and (https://vbpl.moj.gov.vn/huongdan/csdlvbpltrunguong.htm)

## LAW-003 — Công báo điện tử Chính phủ
Official Gazette for verifying publication of promulgated legal instruments and official publication details.
- Portal: https://congbao.chinhphu.vn/
- Status: Official portal; API/runtime not tested. [Source](https://congbao.chinhphu.vn/)

## LAW-004 — Quốc hội Việt Nam
Primary institutional source for National Assembly laws/resolutions, legislative programs and draft legislation. Always distinguish drafts from enacted instruments.
- Portal: https://quochoi.vn/
- Status: Official portal reference; API/runtime not tested.

## LAW-005 — Tòa án nhân dân tối cao / Án lệ
Official judiciary source for published precedents (án lệ), judicial resolutions and guidance. Precedents are not statutes; applicability and status must be checked.
- Portal: https://www.toaan.gov.vn/
- Precedents: https://anle.toaan.gov.vn/
- Status: Official portal reference; API/runtime not tested.

## LAW-006 — Bộ Ngoại giao / Điều ước quốc tế
Official source discovery for treaties involving Vietnam. Verify parties, ratification/approval, entry into force, reservations and current status.
- Portal: https://www.mofa.gov.vn/
- Treaty portal: https://treaty.mofa.gov.vn/
- Status: Official source reference; API/runtime not tested.

## Agent legal-research protocol
1. Identify the legal question, jurisdiction, sector and relevant date.
2. Search official primary sources first: VBPL, Công báo, National Assembly, relevant ministry/agency, judiciary or treaty database.
3. Record document number, issuing body, promulgation date, publication date, effective date, status, amendments/replacements and source URL.
4. Read the full text and relevant transitional provisions; never rely only on search snippets or summaries.
5. Distinguish current consolidated text from original text and each amending instrument. If status is uncertain, label it UNVERIFIED and do not present as current law.
6. Cite the exact source and access date in the Agent's answer. Secondary commercial databases may aid discovery but cannot silently replace official verification.
7. Agent output is legal information/research support, not a substitute for qualified legal advice or an authoritative legal determination.

## Access and execution boundary
All six entries are official-source discovery candidates. This review did not establish public API contracts, bulk export permissions or automated access rights. Do not scrape at scale, bypass controls, submit legal filings or represent a generated summary as an official interpretation.


# RES-25 TO RES-42 — FULL INDUSTRY COVERAGE EXPANSION

## Taxonomy expansion
- **RES-25 Agriculture & Forestry:** crops, livestock, aquaculture, forestry, agricultural prices, agri-tech.
- **RES-26 Industry & Manufacturing:** industrial production, manufacturing, industrial zones, factory automation, quality standards.
- **RES-27 Energy & Power:** electricity, oil and gas, renewables, power grid, energy prices.
- **RES-28 Transport & Logistics:** road, rail, maritime, aviation, ports, freight, supply chain.
- **RES-29 Environment & Climate:** air quality, water quality, climate, emissions, weather observations, carbon.
- **RES-30 Real Estate & Urban Planning:** land, zoning, urban planning, property market, geospatial planning.
- **RES-31 Trade & Retail:** domestic trade, retail, wholesale, e-commerce, consumer markets.
- **RES-32 Tourism & Hospitality:** tourism arrivals, accommodation, tour operators, destinations, tourism statistics.
- **RES-33 Labor & Social Security:** labor force, employment, wages, social insurance, social welfare.
- **RES-34 Insurance:** insurance market, life insurance, non-life insurance, insurance supervision, risk.
- **RES-35 Telecommunications & Media:** telecommunications, broadband, postal services, digital media, ICT indicators.
- **RES-36 Science & Technology:** research, innovation, patents, intellectual property, technology transfer.
- **RES-37 Water & Waste Management:** water resources, water supply, wastewater, solid waste, recycling.
- **RES-38 Food & Food Supply Chain:** food safety, food traceability, food processing, testing, supply chain.
- **RES-39 Corporate Finance, Tax & Accounting:** tax, e-invoices, accounting, audit, business registration, financial statements.
- **RES-40 Human Resources & Enterprise Management:** recruitment, skills, training, HR analytics, enterprise operations.
- **RES-41 Culture & Heritage:** cultural heritage, museums, archives, intangible heritage, digital collections.
- **RES-42 Public Safety & Disaster Risk:** disaster alerts, floods, storms, fire safety, rescue, risk management.

## Seed resource records
### AGR-001 — NSO Vietnam — agriculture, forestry and fishery statistics
- Categories: RES-25, RES-20
- Source: https://www.nso.gov.vn/so-lieu-thong-ke/
- Access: Official statistical tables and reports; API not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Published aggregate statistics; preserve crop/product, geography, season, units and revision dates.

### IND-001 — NSO Vietnam — industrial production statistics
- Categories: RES-26, RES-20
- Source: https://www.nso.gov.vn/so-lieu-thong-ke/
- Access: Official statistical tables and reports; API not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Distinguish industrial production indices, physical output, enterprise counts and survey estimates.

### ENE-001 — NSO Vietnam — energy and electricity statistics
- Categories: RES-27, RES-20
- Source: https://www.nso.gov.vn/so-lieu-thong-ke/
- Access: Official statistical tables and reports; API not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: For operational grid data or real-time dispatch, identify the system operator source separately; NSO tables are not live telemetry.

### LOG-001 — NSO Vietnam — transport and logistics statistics
- Categories: RES-28, RES-20
- Source: https://www.nso.gov.vn/so-lieu-thong-ke/
- Access: Official statistical tables and reports; API not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Preserve transport mode, tonnage/passenger unit, passenger-km/ton-km, geography and reference period.

### ENV-001 — Vietnam environmental statistics and monitoring sources
- Categories: RES-29, RES-37
- Source: https://monre.gov.vn/
- Access: Official ministry portal and linked reports/data systems; public API and sensor feeds not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Do not infer real-time monitor access; record station, pollutant/parameter, unit, calibration and timestamp.

### RE-001 — Vietnam land, planning and urban information source discovery
- Categories: RES-30, RES-11, RES-14
- Source: https://www.monre.gov.vn/
- Access: Official ministry/sector portal discovery; parcel-level open API not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Parcel maps, planning layers and land records may be restricted; verify issuing authority, map scale, coordinate system and effective plan.

### TRD-001 — Ministry of Industry and Trade — domestic market and trade reports
- Categories: RES-31
- Source: https://dms.gov.vn/
- Access: Official reports and portal publications; public data API not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Distinguish official estimates, survey data and platform-reported sales; capture period and methodology.

### TOU-001 — Vietnam National Authority of Tourism — tourism statistics database
- Categories: RES-32, RES-20
- Source: https://thongke.tourism.vn/index.php/
- Access: Public statistical portal; API/export contract not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Portal displays arrivals, domestic tourism and guide statistics; preserve market, transport mode, period and definitions.

### LAB-001 — NSO Vietnam — labor and employment statistics
- Categories: RES-33, RES-20
- Source: https://www.nso.gov.vn/so-lieu-thong-ke/
- Access: Official statistical tables and reports; API not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Aggregate labor indicators only; distinguish labor force, employed, unemployed, underemployment and wage concepts.

### INS-001 — Insurance market regulator and Ministry of Finance publications
- Categories: RES-34, RES-39
- Source: https://www.mof.gov.vn/
- Access: Official regulator/ministry publications; structured API not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Use aggregate market and supervisory data; no policyholder-level or claims personal data.

### TEL-001 — Ministry ICT data portal — telecommunications and digital indicators
- Categories: RES-35, RES-20
- Source: https://data.mst.gov.vn/
- Access: Public dashboard/data portal; API/export details require verification.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Portal categories include telecom, postal, ICT and digital transformation indicators; preserve reporting year and metric definition.

### SCI-001 — Vietnam intellectual property and science-technology source discovery
- Categories: RES-36, RES-14
- Source: https://ipvietnam.gov.vn/
- Access: Official intellectual-property portal; bulk search/API access not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Distinguish application, grant, publication and legal status; preserve applicant/inventor data only under applicable privacy rules.

### WAT-001 — Vietnam water resources and water-sector source discovery
- Categories: RES-37, RES-29
- Source: https://monre.gov.vn/
- Access: Official ministry portal and linked water resources systems; API and sensor access not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Record basin, station, parameter, unit, timestamp, quality flags and authority.

### FOOD-001 — Vietnam food traceability and safety information system
- Categories: RES-38, RES-25
- Source: https://dms.gov.vn/
- Access: Government system described in official legal publication; public query/API and coverage require verification.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Traceability records may be supplied by businesses and are not automatically verified certification; do not infer food safety from a QR code alone.

### TAX-001 — Vietnam Ministry of Finance — tax, e-invoice and enterprise finance source discovery
- Categories: RES-39, RES-13
- Source: https://www.mof.gov.vn/
- Access: Official portal and linked services; public API, access and reuse terms vary and must be verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Tax filing, e-invoice issuance and payment are transactional actions requiring explicit human approval; no credentials in W116.

### HR-001 — VietJobs — Vietnamese job-advertisement research dataset
- Categories: RES-40, RES-33, RES-07
- Source: https://github.com/VinNLP/VietJobs
- Access: Public research dataset/repository; inspect dataset license and download files before reuse.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Research corpus, not a live vacancies feed; check license, collection date, personal data and representativeness before processing.

### CUL-001 — Vietnam cultural heritage and digital archive source discovery
- Categories: RES-41, RES-23
- Source: https://bvhttdl.gov.vn/
- Access: Official ministry portal and linked heritage repositories; open structured API not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Check source institution, provenance, image/text reuse rights, digitization quality and cultural context.

### DRR-001 — Vietnam disaster monitoring and warning source discovery
- Categories: RES-42, RES-29
- Source: https://nchmf.gov.vn/
- Access: Official meteorological and hydrological warning portal; machine API/feed availability not verified.
- Assessment: CANDIDATE / discovery reference only; API, bulk access, terms and runtime remain unverified unless explicitly stated otherwise.
- Guardrail: Use current official warnings and timestamps; distinguish forecast, watch and emergency warning; never delay emergency response for an Agent result.

## Coverage and maturity note
RES-25..RES-42 have been added as industry taxonomy and one discovery seed each. These seeds are not proof of API availability, completeness, freshness, licensing or production readiness. Some official statistical sectors share the NSO portal; domain-specific operational feeds require separate source identification. No runtime tests or authenticated operations were performed in this expansion.
