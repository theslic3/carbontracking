import pytest
from unittest.mock import patch, Mock
from website.dashboard.improvementGeneration import *


def test_generate_footprint_discussion_prompt_with_detailed_input():
    # Input data
    breakdown_facts = {
        'Forecasted Annual Footprint, based on your monthly footprint': 8133.626991250001,
        'Your monthly carbon footprint, in terms of KG of CO released': 677.8022492708334,
        'Average Annual Footprint per person in your region': 6300.0,
        'Average Annual Footprint per person in the UK ': 6500.0,
        'Your household disposable income categorises you as': 'Very High',
        'Your Recycling Status': 'no',
        'Your Household Size': 4
    }

    # Generate prompt
    result = generate_footprint_discussion_prompt(breakdown_facts)

    # Verify expected content
    assert "8133.626991250001" in result
    assert "6500.0" in result
    assert "Very High" in result


def test_generate_footprint_discussion_prompt():
    # Input data using provided breakdown facts
    breakdown_facts = (
        "Forecasted Annual Footprint, based on your monthly footprint: 8133.626991250001 kg, "
        "Your monthly carbon footprint, in terms of KG of CO released: 677.8022492708334 kg, "
        "Average Annual Footprint per person in your region: 6300.0 kg, "
        "Average Annual Footprint per person in the UK: 6500.0 kg, "
        "Your household disposable income categorises you as: Very High, "
        "Your Recycling Status: no, "
        "Your Household Size: 4"
    )

    # Expected format checking
    result = generate_footprint_discussion_prompt(breakdown_facts)

    # Assertions to check if the returned prompt includes the necessary data
    assert "8133.626991250001 kg" in result
    assert "6300.0 kg" in result
    assert "6500.0 kg" in result
    assert "Very High" in result
    assert "no" in result
    assert "4" in result

@patch('website.dashboard.improvementGeneration.client.chat.completions.create')
def test_generate_suggestions_success(mock_completions_create):
    # Setup mock to return a controlled response
    mock_response = Mock()
    mock_response.choices = [Mock(message=Mock(content="This is a sample response"))]
    mock_completions_create.return_value = mock_response

    # Call the function with a test prompt
    prompt = "Sample prompt"
    response = generate_suggestions(prompt)

    # Check if the response matches the mock
    assert response == "This is a sample response"
    mock_completions_create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly carbon footprint expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

@patch('website.dashboard.improvementGeneration.client.chat.completions.create')
def test_generate_suggestions_failure(mock_completions_create):
    # Setup mock to raise an exception
    mock_completions_create.side_effect = Exception("API error")

    # Call the function with a test prompt
    prompt = "Sample prompt"
    response = generate_suggestions(prompt)

    # Check if the response matches the failure case
    assert response == "Improvements cannot be generated at this time. Please try again later!"
    mock_completions_create.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly carbon footprint expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
