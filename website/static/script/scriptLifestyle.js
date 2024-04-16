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
