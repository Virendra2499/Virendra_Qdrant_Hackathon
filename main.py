
from qdrant_client import QdrantClient
from langchain.schema import Document
from langchain.vectorstores import Qdrant
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from google.colab import userdata
userdata.get('secretName')
import os

# Setup Qdrant
qdrant_client = QdrantClient(
    url= url, 
    api_key= QDRANT_API_KEY,
)


# Setup embeddings: Hugging Face
hf_embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
# Optionally, Google Generative AI embeddings (if available for embeddings)
ggai_embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-2.5-pro")  # if embedding capability is supported

# Your product docs to store
our_products = [
    {"sku": "Y001", "desc": "Electrolytic Capacitor 100µF ±10%, 50V, radial, Ø5mm ×11mm"},
    {"sku": "Y002", "desc": "Electrolytic Capacitor 220µF ±20%, 25V, radial, Ø6.3mm ×11mm"},
    {"sku": "Y003", "desc": "Resistor 10kΩ ±1%, 0.25W, axial"},
    {"sku": "Y004", "desc": "MOSFET IRF540N N-Channel, 100V, 33A, Rds(on)=0.077Ω"},
    {"sku": "Y005", "desc": "Stepper Motor NEMA17, 1.8° step, 45N·cm torque, 2A"},
    {"sku": "Y006", "desc": "Microcontroller ATmega328P 8-bit, 32KB Flash, 20MHz"},
    {"sku": "Y007", "desc": "Diode 1N4007, 1A, 1000V, DO-41"},
    {"sku": "Y008", "desc": "Optocoupler PC817, CTR 50-600%, 5kV isolation"},
    {"sku": "Y009", "desc": "Relay 5V SPDT, coil 5V, 10A contact"},
    {"sku": "Y010", "desc": "Voltage Regulator LM7805, fixed 5V output, TO-220, ~1A"},
]

# Create Documents
docs = [Document(page_content=p["desc"], metadata={"sku": p["sku"]}) for p in our_products]

# Create vector store with HF embeddings
vectorstore = Qdrant.from_documents(
    documents=docs,
    embedding=hf_embedding_model,
    url=":memory:" ,# in memory
    prefer_grpc=False,
    collection_name="our_products_hf"
)

# If you want, also create a second collection using Gemini embeddings (if you have embedding access)
# vectorstore_ggai = Qdrant.from_documents(
#     documents=docs,
#     embedding=ggai_embedding_model,
#     url=":memory:",
#     collection_name="our_products_ggai"
# )

# Competitor items to query
competitors = [
    {"sku": "C101", "desc": "Electrolytic Capacitor 100µF ±10%, 50V, radial, Ø5×11mm"},
    {"sku": "C104", "desc": "MOSFET IRF540 N-Channel, 100V, 33A, Rds(on)=0.080Ω"},
    {"sku": "C105", "desc": "Stepper Motor NEMA17, 1.8° step, 50N·cm torque, 1.7A"},
    {"sku": "C106", "desc": "ATmega328 MCU 8-bit, 32KB Flash, 16MHz"},
    {"sku": "C108", "desc": "Optocoupler PC817C, CTR 50-600%, 5kV isolation"},
    {"sku": "C110", "desc": "LM7805 fixed 5V output regulator TO-220"},
]

# Function to compute matches
matches = []
for comp in competitors:
    result = vectorstore.similarity_search_with_score(comp["desc"], k=1)
    matched_doc, score = result[0]
    matches.append({
        "competitor_sku": comp["sku"],
        "competitor_desc": comp["desc"],
        "our_sku": matched_doc.metadata["sku"],
        "our_desc": matched_doc.page_content,
        "hf_similarity_score": score
    })

# Optionally: Use Gemini (via LangChain) to refine, explain, or produce summary
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY  # needed for google-genai
gen_ai_llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")

# Example: ask it to explain why some matches are weaker or differences
for m in matches:
    prompt = f"""
    I have this competitor component: "{m['competitor_desc']}".
    I matched it to our component: "{m['our_desc']}" with similarity score {m['hf_similarity_score']:.2f}.
    Please analyze the differences in specs, and tell me whether this match is good, and what are the spec-gaps.
    """
    explanation = gen_ai_llm.invoke(prompt)
    m["explanation"] = explanation.text

# Print output

for m in matches:
    print("Competitor SKU:", m["competitor_sku"])
    print("Our SKU:", m["our_sku"])
    print("HF Similarity:", m["hf_similarity_score"])
    print("Explanation:", m["explanation"])
    print("----")
