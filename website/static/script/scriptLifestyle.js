let currentStep = 0;
const form = document.getElementById('carbonForm');
const steps = document.querySelectorAll('.step');

// Function to show current step and hide others
function showStep(stepIndex) {
  steps.forEach((step, index) => {
    if (index === stepIndex) {
      step.style.display = 'block';
    } else {
      step.style.display = 'none';
    }
  });
}

// Function to navigate to the next step
function nextStep() {
  if (currentStep < steps.length - 1) {
    currentStep++;
    showStep(currentStep);
  }
}

// Function to navigate to the previous step
function prevStep() {
  if (currentStep > 0) {
    currentStep--;
    showStep(currentStep);
  }
}

// Initially hide all steps except the first one
showStep(currentStep);

document.getElementById('householdIncome').addEventListener('input', function() {
  document.getElementById('householdIncomeValue').innerText = this.value;
});

/*
// Add event listener for form submission
form.addEventListener('submit', function(event) {
  event.preventDefault();
  // Collect form data
  const formData = {};
  const inputs = form.querySelectorAll('input, select');
  inputs.forEach(input => {
    formData[input.name] = input.value;
  });

  const jsonData = JSON.stringify(formData);
  console.log(jsonData);
  let xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/retrieveCalculation", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send(jsonData);

  return false;

  // Here you can handle the JSON data as needed, such as sending it to a server
});
*/
