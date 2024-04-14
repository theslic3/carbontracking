from openai import OpenAI
OPENAI_API_KEY = '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'
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_lifestyle_improvements_prompt(breakdown_facts, three_highest_emissions):

    prompt = """
    Given the following user profile:

    User Profile:
    {breakdown_facts}

    And the three highest emission categories are:

    1. {emission_1_factor}: {emission_1_value}
    2. {emission_2_factor}: {emission_2_value}
    3. {emission_3_factor}: {emission_3_value}

    Generate an actionable plan for lifestyle improvements, focussing on each of the three highest emission factors.
    Make sure to tailor response to the my income category. Ensure to paragraph and linebreak appropriately.
    """
    # Formatting the emission factors and values
    emission_1_factor, emission_1_value = three_highest_emissions[0]
    emission_2_factor, emission_2_value = three_highest_emissions[1]
    emission_3_factor, emission_3_value = three_highest_emissions[2]

    # Fill in the prompt with the user profile and emissions information
    filled_prompt = prompt.format(
        breakdown_facts=breakdown_facts,
        emission_1_factor=emission_1_factor,
        emission_1_value=emission_1_value,
        emission_2_factor=emission_2_factor,
        emission_2_value=emission_2_value,
        emission_3_factor=emission_3_factor,
        emission_3_value=emission_3_value
    )

    emission_1_factor, emission_1_value = three_highest_emissions[0]
    emission_2_factor, emission_2_value = three_highest_emissions[1]
    emission_3_factor, emission_3_value = three_highest_emissions[2]

    # Fill in the prompt with the user profile and emissions information
    filled_prompt = prompt.format(
        breakdown_facts=breakdown_facts,
        emission_1_factor=emission_1_factor,
        emission_1_value=emission_1_value,
        emission_2_factor=emission_2_factor,
        emission_2_value=emission_2_value,
        emission_3_factor=emission_3_factor,
        emission_3_value=emission_3_value
    )

    return filled_prompt

def generate_footprint_discussion_prompt(breakdown_facts):

    prompt = """
    Given the following user profile:

    User Profile:
    {breakdown_facts}

    Give a brief discussion of my annual forecasted carbon footprint, in comparison to the UK and my region.
    Keep this discussion to 50 words. Don't mention improvements, keep it to facts.
    Ensure to paragraph and linebreak appropriately.
    """

    # Fill in the prompt with the user profile and emissions information
    filled_prompt = prompt.format(
        breakdown_facts=breakdown_facts
    )

    return filled_prompt


def generate_suggestions(prompt):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly carbon footprint expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Improvements cannot be generated at this time. Please try again later!"
