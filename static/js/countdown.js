document.addEventListener('DOMContentLoaded', () => {
  const countdownContainer = document.querySelector('.countdown');
  if (!countdownContainer) return;

  const countdownDateString = countdownContainer.getAttribute('data-countdown');
  const countdownDate = new Date(countdownDateString).getTime();

  const daysElement = countdownContainer.querySelector('[data-d]');
  const hoursElement = countdownContainer.querySelector('[data-h]');
  const minutesElement = countdownContainer.querySelector('[data-m]');
  const secondsElement = countdownContainer.querySelector('[data-s]');

  const updateCountdown = () => {
    const now = new Date().getTime();
    const distance = countdownDate - now;

    if (distance < 0) {
      clearInterval(intervalId);
      if (daysElement) daysElement.innerText = '00';
      if (hoursElement) hoursElement.innerText = '00';
      if (minutesElement) minutesElement.innerText = '00';
      if (secondsElement) secondsElement.innerText = '00';
      return;
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    if (daysElement) daysElement.innerText = String(days).padStart(2, '0');
    if (hoursElement) hoursElement.innerText = String(hours).padStart(2, '0');
    if (minutesElement) minutesElement.innerText = String(minutes).padStart(2, '0');
    if (secondsElement) secondsElement.innerText = String(seconds).padStart(2, '0');
  };

  updateCountdown();
  const intervalId = setInterval(updateCountdown, 1000);
});