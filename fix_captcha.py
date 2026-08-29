path = "src/components/CaptchaWidget.tsx"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_slider = """  const handleSliderComplete = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/auth/verify-captcha', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token: `wejobs_token_${Date.now()}`,
          answer: 'HUMAN_CONFIRMED',
        }),
      });
      const data = await response.json();
      if (data.success && data.verifiedToken) {
        setVerified(true);
        onVerified(data.verifiedToken);
      } else {
        setError(data.error || 'Verification failed. Please try again.');
        setSliderPosition(0);
      }
    } catch (err) {
      setError('Network error verifying challenge.');
      setSliderPosition(0);
    } finally {
      setLoading(false);
    }
  };"""

new_slider = """  const handleSliderComplete = () => {
    setLoading(true);
    setError(null);
    setTimeout(() => {
      const token = `wejobs_client_token_${Date.now()}`;
      setVerified(true);
      onVerified(token);
      setLoading(false);
    }, 300);
  };"""

if old_slider in content:
    content = content.replace(old_slider, new_slider, 1)
    print("[OK] handleSliderComplete berhasil diganti (client-side).")
else:
    print("[GAGAL] handleSliderComplete tidak ketemu.")

old_math = """  const handleMathVerify = async () => {
    const expected = challengeNumberA + challengeNumberB;
    if (parseInt(userMathAnswer, 10) !== expected) {
      setError('Incorrect math answer. Please try again.');
      setUserMathAnswer('');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/auth/verify-captcha', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          token: `wejobs_token_${Date.now()}`,
          answer: userMathAnswer,
        }),
      });
      const data = await response.json();
      if (data.success && data.verifiedToken) {
        setVerified(true);
        onVerified(data.verifiedToken);
      } else {
        setError(data.error || 'Verification failed.');
      }
    } catch (err) {
      setError('Network error verifying security token.');
    } finally {
      setLoading(false);
    }
  };"""

new_math = """  const handleMathVerify = () => {
    const expected = challengeNumberA + challengeNumberB;
    if (parseInt(userMathAnswer, 10) !== expected) {
      setError('Incorrect math answer. Please try again.');
      setUserMathAnswer('');
      return;
    }
    setLoading(true);
    setError(null);
    setTimeout(() => {
      const token = `wejobs_client_token_${Date.now()}`;
      setVerified(true);
      onVerified(token);
      setLoading(false);
    }, 300);
  };"""

if old_math in content:
    content = content.replace(old_math, new_math, 1)
    print("[OK] handleMathVerify berhasil diganti (client-side).")
else:
    print("[GAGAL] handleMathVerify tidak ketemu.")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
