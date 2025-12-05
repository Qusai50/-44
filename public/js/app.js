// Handle contact form submission
document.getElementById('contactForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const data = {
    name: form.name.value || '',
    email: form.email.value,
    message: form.message.value
  };
  try {
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    const j = await res.json();
    if (res.ok) {
      alert('تم إرسال الرسالة بنجاح!');
      form.reset();
    } else {
      alert('خطأ: ' + (j.error || 'فشل الإرسال'));
    }
  } catch (err) {
    alert('خطأ في الاتصال: ' + err.message);
  }
});
