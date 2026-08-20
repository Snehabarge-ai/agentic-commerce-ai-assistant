import json
import re
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Load environment variables from backend/.env
load_dotenv(Path(__file__).parent / ".env")

# Gemini client
client = genai.Client()


# Load product catalog
PRODUCTS = json.loads(
    (Path(__file__).parent / "products.json").read_text(encoding="utf-8")
)


# Product categories
CATS = {
    "headphones": ["headphone", "earphone", "earbuds", "audio"],
    "laptop": ["laptop", "notebook", "computer"],
    "phone": ["phone", "smartphone", "mobile"],
}

# Common use cases
USES = [
    "travel",
    "music",
    "office",
    "coding",
    "development",
    "college",
    "camera",
    "gaming",
]


def intent(q):
    """Extract basic shopping intent from the user query."""

    q = q.lower()

    # Detect category
    cat = next(
        (
            c
            for c, words in CATS.items()
            if any(word in q for word in words)
        ),
        None,
    )

    # Detect budget
    match = re.search(
        r"(?:under|below|upto|up to|less than)\s*[₹$]?\s*(\d+)\s*(k|thousand|lakh)?",
        q,
    )

    budget = None

    if match:
        budget = float(match.group(1))

        if match.group(2) in ("k", "thousand"):
            budget *= 1000
        elif match.group(2) == "lakh":
            budget *= 100000

    return {
        "category": cat,
        "budget": budget,
        "use_cases": [u for u in USES if u in q],
    }


def generate_ai_recommendation(query, intent_data, products):
    """
    Use Gemini to explain why the top product is suitable.
    Gemini is instructed to use only products supplied by our catalog.
    """

    if not products:
        return "No matching products were found in the catalog."

    product_context = []

    for product in products:
        product_context.append(
            {
                "name": product.get("name"),
                "category": product.get("category"),
                "price": product.get("price"),
                "rating": product.get("rating"),
                "use_case": product.get("use_case"),
                "specs": product.get("specs"),
            }
        )

    prompt = f"""
You are an AI shopping recommendation agent.

User query:
{query}

Extracted intent:
{json.dumps(intent_data, indent=2)}

Candidate products from our catalog:
{json.dumps(product_context, indent=2)}

Choose the best product ONLY from the candidate products.

Explain the recommendation in 2-4 concise sentences.

Your explanation must:
- Respect the user's budget if one exists.
- Consider the requested category.
- Consider the user's use case.
- Mention the main reason the selected product is a good choice.
- Never invent specifications, prices, ratings, or products.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt,
        )

        return response.text.strip()

    except Exception as e:
        print("Gemini API error:", e)

        # Graceful fallback so the application still works
        best = products[0]

        return (
            f"{best['name']} is the top match based on the "
            f"available catalog, rating, budget and requested use case."
        )


def run(q):
    """Run the complete shopping agent pipeline."""

    # 1. Intent extraction
    i = intent(q)

    # 2. Catalog search + constraint filtering
    filtered_products = [
        p
        for p in PRODUCTS
        if (
            not i["category"]
            or p["category"] == i["category"]
        )
        and (
            not i["budget"]
            or p["price"] <= i["budget"]
        )
    ]

    # 3. Product ranking
    for product in filtered_products:
        product["_score"] = (
            product["rating"]
            + sum(
                0.8
                for use_case in i["use_cases"]
                if use_case in product["use_case"]
            )
        )

    ranked_products = sorted(
        filtered_products,
        key=lambda p: p["_score"],
        reverse=True,
    )[:4]

    # Fallback if no products satisfy the constraints
    if not ranked_products:
        ranked_products = sorted(
            PRODUCTS,
            key=lambda p: p["rating"],
            reverse=True,
        )[:4]

    # Remove temporary ranking field
    for product in ranked_products:
        product.pop("_score", None)

    # 4. Gemini recommendation explanation
    ai_explanation = generate_ai_recommendation(
        q,
        i,
        ranked_products,
    )

    # 5. Final agent response
    return {
        "query": q,
        "intent": i,
        "recommendation": ranked_products[0],
        "alternatives": ranked_products[1:],
        "ai_explanation": ai_explanation,
        "agent_steps": [
            "Intent extraction",
            "Catalog search",
            "Constraint filtering",
            "Product ranking",
            "AI recommendation generation",
        ],
    }