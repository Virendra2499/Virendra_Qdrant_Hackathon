📑 Project Report

Project Title:
AI-Powered Product Matching & Dynamic Pricing for Mechatronics Components

1️⃣ Executive Summary

The mechatronics and electronics component market is highly fragmented, with thousands of SKUs and very subtle differences in part numbers, tolerances, and specs.
Traditional manual mapping of competitor products to internal catalog is slow, error-prone, and does not scale.

This project leverages Retrieval-Augmented Generation (RAG), Hugging Face open-source embedding models, Qdrant vector database, and Google Gemini LLM to automate competitor product matching, spec comparison, and pricing analytics.

2️⃣ Real-Life Problem
Challenges Faced by Distributors / Retailers:

Huge SKU Catalog: 10,000+ parts, each with multiple dimensions/specs.

Manual Search Overhead: Engineers waste hours finding which competitor part matches yours.

Pricing Blindspots: Competitors change price dynamically — hard to respond quickly.

Missed Revenue: Without quick adjustments, you either:

Lose customers (price too high)

Lose margin (price too low unnecessarily)

Business Impact of Current Approach:

Time Lost: ~10–15 mins per SKU to map competitor item manually

Error Rate: Human matching errors ~20% (wrong part → wrong pricing decision)

Slow Price Response: Competitors adjust price daily, your team updates weekly → lost sales opportunities

3️⃣ Proposed Solution
Goal:

Automate competitor product mapping + pricing insights using AI-driven similarity search + LLM reasoning.

Solution Architecture

1. Data Ingestion

Your product catalog (SKU, specs, cost price, inventory, min margin)

Competitor scraped catalog (SKU, specs, price, availability)

2. Embedding + Vector Store

Use Hugging Face Embedding Model (all-mpnet-base-v2 or BAAI/bge-base-en-v1.5)

Convert product specs into embeddings (dense vectors)

Store in Qdrant vector DB for fast semantic search

3. Retrieval

For each competitor product:

Perform similarity search against your catalog

Retrieve top-N potential matches

4. Reasoning & Enrichment

Use Google Gemini (via LangChain) to:

Explain differences in specs

Flag mismatches (e.g., voltage mismatch, tolerance difference)

Recommend if match is acceptable

5. Pricing Analytics

Calculate profit margin if priced at competitor price:

Margin
=
Price
−
Cost Price
Cost Price
×
100
Margin=
Cost Price
Price−Cost Price
	​

×100

Generate pricing recommendation (e.g., match competitor ±X%, protect minimum margin)

6. Output Dashboard

Show matched pairs, similarity score, recommended price, risk flags, explanation.

4️⃣ Technology Choices
Component	Choice	Reason
Embedding Model	Hugging Face all-mpnet-base-v2	Open-source, robust semantic search performance
Vector Database	Qdrant	Open-source, scalable, easy integration with LangChain
Orchestration	LangChain	Abstracts retriever + LLM workflow
LLM Reasoning	Google Gemini (via langchain-google-genai)	Provides natural language reasoning, spec comparison, explanations
Deployment	Python + REST API + Dashboard (Streamlit/React)	Easy integration with internal systems
5️⃣ Mathematical Approach

Embedding Similarity
Use cosine similarity between competitor product vector 
𝑐
⃗
c
 and each of your product vectors 
𝑝
⃗
p
	​

:

sim
(
𝑐
⃗
,
𝑝
⃗
)
=
𝑐
⃗
⋅
𝑝
⃗
∥
𝑐
⃗
∥
∥
𝑝
⃗
∥
sim(
c
,
p
	​

)=
∥
c
∥∥
p
	​

∥
c
⋅
p
	​

	​


Choose top-k matches with highest similarity score.

Spec Gap Scoring
If needed, compute spec-by-spec differences (voltage, tolerance, size) → generate weighted similarity:

SpecScore
=
∑
𝑤
𝑖
⋅
match
(
𝑠
𝑝
𝑒
𝑐
𝑖
)
SpecScore=∑w
i
	​

⋅match(spec
i
	​

)

Composite Score:

Composite
=
𝛼
⋅
EmbeddingSim
+
(
1
−
𝛼
)
⋅
SpecScore
Composite=α⋅EmbeddingSim+(1−α)⋅SpecScore

Pricing Recommendation
Adjust price if margin allows:

Recommended Price
=
{
Competitor Price
−
𝛿
	
if inventory is high


Competitor Price
+
𝜖
	
if inventory is low
Recommended Price={
Competitor Price−δ
Competitor Price+ϵ
	​

if inventory is high
if inventory is low
	​

6️⃣ Input / Output Example
Input:

Your catalog (10 SKUs) + competitor catalog (10 SKUs)

Processing Result (Dummy Output)
Competitor SKU	Competitor Desc	Our SKU	Our Desc	Similarity	Gemini Explanation	Recommended Price
C101	Capacitor 100µF ±10%, 50V	Y001	Capacitor 100µF ±10%, 50V	0.95	Perfect match, same dimensions/specs	Match competitor price (₹8.50/unit)
C104	MOSFET IRF540	Y004	MOSFET IRF540N, Rds=0.077Ω	0.88	Ours has slightly lower Rds(on), better performance	Maintain price at +3% premium
C105	Stepper Motor NEMA17	Y005	NEMA17 45N·cm torque	0.86	Competitor has slightly higher torque rating	Match competitor price if inventory > 100
C106	ATmega328	Y006	ATmega328P 20 MHz	0.82	Ours has higher clock speed, better performance	Keep price slightly higher
7️⃣ Business Impact
Key Benefits

✅ 95% Faster Product Matching – no manual spreadsheet work
✅ Reduced Pricing Errors – AI ensures spec match before pricing
✅ Dynamic Competitor Response – adjust price daily/weekly
✅ Inventory Optimization – drop price when stock is high → improve cash flow

ROI Calculation (Example)

Time Saved:

Old process: 10 mins/SKU × 5000 SKUs = 833 hours/month

AI-assisted: <1 min/SKU = 83 hours/month

750 engineer-hours saved/month → if engineer cost = $30/hr → $22,500/month saved

Revenue Gain:

Faster price match → recover lost sales opportunities (~5% extra sales)

On $200k monthly revenue → +$10k/month

Net Impact:

ROI
=
Monthly Gain
−
Cost
Cost
ROI=
Cost
Monthly Gain−Cost
	​


If cost to run is $5k/month →
ROI ≈ (22,500 + 10,000 – 5,000) / 5,000 = 5.4× return

8️⃣ Conclusion

This project directly impacts revenue and profitability by enabling:

Faster and more accurate product mapping

Smarter and more competitive pricing decisions

Better use of inventory

Time saving for engineers & pricing team

By leveraging open-source embeddings (Hugging Face) + scalable vector DB (Qdrant) + reasoning power of Gemini LLM, we create a production-grade, explainable, and cost-efficient solution.
