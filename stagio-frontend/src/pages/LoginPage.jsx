// src/pages/LoginPage.jsx
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import styled, { ThemeProvider } from "styled-components";
import { darkTheme, lightTheme, GlobalStyle, PageBg, BlobMid, Above, fadeUp, ErrorMsg, Input, Label, FormGroup, PrimaryButton } from "../theme";
import { useAuth } from "../context/AuthContext";

const Card = styled.div`
  width: 100%; max-width: 420px;
  background: ${({ theme }) => theme.bgCard};
  backdrop-filter: blur(28px);
  border: 1px solid ${({ theme }) => theme.border};
  border-radius: 20px; padding: 44px 36px;
  position: relative; overflow: hidden;
  animation: ${fadeUp} 0.5s ease;
  &::before {
    content: '';
    position: absolute; top: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, ${({ theme }) => theme.accent}, transparent);
  }
`;
const Center = styled.div`
  min-height: 100vh; display: flex;
  align-items: center; justify-content: center; padding: 24px;
`;
const LogoSquare = styled.div`
  width: 44px; height: 44px;
  background: ${({ theme }) => theme.accentGrad};
  border-radius: 12px; margin: 0 auto 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; font-weight: 700; color: #fff;
  box-shadow: 0 0 20px ${({ theme }) => theme.accentGlow};
`;
const LogoName = styled.h1`font-size: 20px; font-weight: 700; color: ${({ theme }) => theme.text}; letter-spacing: -0.3px; text-align: center;`;
const LogoSub  = styled.p`font-size: 12px; color: ${({ theme }) => theme.textMuted}; margin-top: 3px; text-align: center; margin-bottom: 28px;`;
const Title    = styled.h2`font-size: 22px; font-weight: 700; color: ${({ theme }) => theme.text}; letter-spacing: -0.4px; margin-bottom: 4px;`;
const TitleSub = styled.p`font-size: 13px; color: ${({ theme }) => theme.textMuted}; margin-bottom: 28px;`;
const SubmitBtn = styled(PrimaryButton)`width: 100%; padding: 12px; font-size: 14px; margin-top: 6px;`;
const Divider = styled.div`
  display: flex; align-items: center; gap: 12px; margin: 24px 0;
  &::before, &::after { content: ''; flex: 1; height: 1px; background: ${({ theme }) => theme.border}; }
  span { font-size: 12px; color: ${({ theme }) => theme.textFaint}; white-space: nowrap; }
`;
const FooterText = styled.p`
  text-align: center; font-size: 13px; color: ${({ theme }) => theme.textMuted};
  a { color: ${({ theme }) => theme.accent}; text-decoration: none; font-weight: 500; }
  a:hover { color: ${({ theme }) => theme.accentPink}; }
`;
const ThemeBtn = styled.button`
  position: absolute; top: 16px; right: 16px;
  padding: 5px 12px; background: ${({ theme }) => theme.bgBtn};
  border: 1px solid ${({ theme }) => theme.borderBtn};
  border-radius: 20px; font-size: 11px; color: ${({ theme }) => theme.textMuted};
  font-family: 'DM Sans', sans-serif; cursor: pointer; transition: all 0.2s;
  &:hover { border-color: ${({ theme }) => theme.accent}; color: ${({ theme }) => theme.text}; }
`;

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [isDark, setIsDark]     = useState(true);
  const [form, setForm]         = useState({ email: "", password: "" });
  const [error, setError]       = useState("");
  const [loading, setLoading]   = useState(false);
  const theme = isDark ? darkTheme : lightTheme;

  const handleChange = (e) => { setForm(p => ({ ...p, [e.target.name]: e.target.value })); setError(""); };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.email || !form.password) { setError("Please fill in all fields."); return; }
    setLoading(true);
    try {
      await login(form.email, form.password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid email or password.");
    } finally { setLoading(false); }
  };

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <PageBg>
        <BlobMid />
        <Above>
          <Center>
            <Card>
              <ThemeBtn onClick={() => setIsDark(p => !p)}>{isDark ? "☀ Light" : "🌙 Dark"}</ThemeBtn>
              <LogoSquare>S</LogoSquare>
              <LogoName>STAG.IO</LogoName>
              <LogoSub>Internship Management Platform</LogoSub>
              <Title>Welcome back</Title>
              <TitleSub>Sign in to your account to continue</TitleSub>
              {error && <ErrorMsg>{error}</ErrorMsg>}
              <form onSubmit={handleSubmit}>
                <FormGroup>
                  <Label>Email address</Label>
                  <Input type="email" name="email" placeholder="you@university.dz" value={form.email} onChange={handleChange} />
                </FormGroup>
                <FormGroup>
                  <Label>Password</Label>
                  <Input type="password" name="password" placeholder="••••••••" value={form.password} onChange={handleChange} />
                </FormGroup>
                <SubmitBtn type="submit" disabled={loading}>{loading ? "Signing in..." : "Sign In →"}</SubmitBtn>
              </form>
              <Divider><span>New here?</span></Divider>
              <FooterText>
                Register as <Link to="/register/student">Student</Link> or <Link to="/register/company">Company</Link>
              </FooterText>
            </Card>
          </Center>
        </Above>
      </PageBg>
    </ThemeProvider>
  );
}
