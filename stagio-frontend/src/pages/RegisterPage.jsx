// src/pages/RegisterPage.jsx
import { useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import styled, { ThemeProvider } from "styled-components";
import { darkTheme, lightTheme, GlobalStyle, PageBg, BlobMid, Above, fadeUp, ErrorMsg, SuccessMsg, Input, Label, FormGroup, FormRow, PrimaryButton } from "../theme";
import api from "../api/axios";

const Card = styled.div`
  width: 100%; max-width: 480px;
  background: ${({ theme }) => theme.bgCard};
  backdrop-filter: blur(28px);
  border: 1px solid ${({ theme }) => theme.border};
  border-radius: 20px; padding: 40px 36px;
  position: relative; overflow: hidden;
  animation: ${fadeUp} 0.5s ease;
  &::before {
    content: '';
    position: absolute; top: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, ${({ theme }) => theme.accentPink}, transparent);
  }
`;
const Center = styled.div`
  min-height: 100vh; display: flex;
  align-items: center; justify-content: center; padding: 24px;
`;
const LogoSquare = styled.div`
  width: 36px; height: 36px;
  background: ${({ theme }) => theme.accentGrad};
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 700; color: #fff;
  box-shadow: 0 0 16px ${({ theme }) => theme.accentGlow};
`;
const LogoRow = styled.div`display: flex; align-items: center; gap: 10px; margin-bottom: 24px;`;
const LogoName = styled.span`font-size: 17px; font-weight: 700; color: ${({ theme }) => theme.text};`;
const TabRow = styled.div`
  display: grid; grid-template-columns: 1fr 1fr;
  background: ${({ theme }) => theme.bgBtn};
  border: 1px solid ${({ theme }) => theme.border};
  border-radius: 12px; padding: 4px; margin-bottom: 24px;
`;
const Tab = styled.button`
  padding: 9px; border-radius: 9px; border: none;
  background: ${({ $active, theme }) => $active ? theme.bgStat : 'transparent'};
  border: 1px solid ${({ $active, theme }) => $active ? theme.borderBtn : 'transparent'};
  color: ${({ $active, theme }) => $active ? theme.text : theme.textMuted};
  font-family: 'DM Sans', sans-serif; font-size: 13px;
  font-weight: ${({ $active }) => $active ? '600' : '400'};
  cursor: pointer; transition: all 0.2s;
`;
const Title = styled.h2`font-size: 20px; font-weight: 700; color: ${({ theme }) => theme.text}; letter-spacing: -0.4px; margin-bottom: 4px;`;
const TitleSub = styled.p`font-size: 13px; color: ${({ theme }) => theme.textMuted}; margin-bottom: 24px;`;
const SubmitBtn = styled(PrimaryButton)`width: 100%; padding: 12px; font-size: 14px; margin-top: 4px;`;
const FooterText = styled.p`
  text-align: center; font-size: 13px; color: ${({ theme }) => theme.textMuted}; margin-top: 20px;
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
const Note = styled.p`font-size: 11px; color: ${({ theme }) => theme.textFaint}; margin-top: 4px;`;

export default function RegisterPage() {
  const navigate = useNavigate();
  const { type } = useParams();
  const isCompany = type === "company";
  const [isDark, setIsDark] = useState(true);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const theme = isDark ? darkTheme : lightTheme;

  const [sForm, setSForm] = useState({ first_name: "", last_name: "", wilaya: "", email: "", password: "", confirm_password: "" });
  const [cForm, setCForm] = useState({ company_name: "", email: "", password: "", confirm_password: "", phone: "", address: "" });

  const handleS = (e) => { setSForm(p => ({ ...p, [e.target.name]: e.target.value })); setError(""); };
  const handleC = (e) => { setCForm(p => ({ ...p, [e.target.name]: e.target.value })); setError(""); };

  const submitStudent = async (e) => {
    e.preventDefault();
    if (sForm.password !== sForm.confirm_password) { setError("Passwords don't match."); return; }
    setLoading(true);
    try {
      await api.post("/api/user/register/student/", {
        full_name: `${sForm.first_name} ${sForm.last_name}`,
        email: sForm.email,
        password: sForm.password,
        wilaya: sForm.wilaya || "Algiers" // Default just in case
      });
      setSuccess("Account created! Redirecting to login...");
      setTimeout(() => navigate("/login"), 2000);
    } catch (err) {
      const d = err.response?.data;
      setError(typeof d === "object" ? Object.values(d).flat().join(" ") : "Registration failed.");
    } finally { setLoading(false); }
  };

  const submitCompany = async (e) => {
    e.preventDefault();
    if (cForm.password !== cForm.confirm_password) { setError("Passwords don't match."); return; }
    setLoading(true);
    try {
      await api.post("/api/user/register/company/", {
        name: cForm.company_name,
        email: cForm.email,
        password: cForm.password,
        wilaya: cForm.address || "Algiers",
        description: cForm.phone ? `Phone: ${cForm.phone}` : ""
      });
      setSuccess("Company registered! Redirecting to login...");
      setTimeout(() => navigate("/login"), 2000);
    } catch (err) {
      const d = err.response?.data;
      setError(typeof d === "object" ? Object.values(d).flat().join(" ") : "Registration failed.");
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
              <LogoRow>
                <LogoSquare>S</LogoSquare>
                <LogoName>STAG.IO</LogoName>
              </LogoRow>
              <TabRow>
                <Tab $active={!isCompany} onClick={() => navigate("/register/student")} type="button">Student</Tab>
                <Tab $active={isCompany} onClick={() => navigate("/register/company")} type="button">Company</Tab>
              </TabRow>
              <Title>{isCompany ? "Register Company" : "Create Account"}</Title>
              <TitleSub>{isCompany ? "Post offers and find talented students" : "Find the perfect internship"}</TitleSub>
              {error && <ErrorMsg>{error}</ErrorMsg>}
              {success && <SuccessMsg>{success}</SuccessMsg>}

              {!isCompany && (
                <form onSubmit={submitStudent}>
                  <FormRow>
                    <FormGroup><Label>First Name</Label><Input name="first_name" placeholder="Ahmed" value={sForm.first_name} onChange={handleS} required /></FormGroup>
                    <FormGroup><Label>Last Name</Label><Input name="last_name" placeholder="Benali" value={sForm.last_name} onChange={handleS} required /></FormGroup>
                  </FormRow>
                  <FormRow>
                    <FormGroup>
                      <Label>University Email</Label>
                      <Input type="email" name="email" placeholder="a.benali@univ.dz" value={sForm.email} onChange={handleS} required />
                      <Note>Use your university email if possible</Note>
                    </FormGroup>
                    <FormGroup>
                      <Label>Wilaya</Label>
                      <Input name="wilaya" placeholder="Algiers, Oran..." value={sForm.wilaya} onChange={handleS} required />
                    </FormGroup>
                  </FormRow>
                  <FormRow>
                    <FormGroup><Label>Password</Label><Input type="password" name="password" placeholder="••••••••" value={sForm.password} onChange={handleS} required /></FormGroup>
                    <FormGroup><Label>Confirm</Label><Input type="password" name="confirm_password" placeholder="••••••••" value={sForm.confirm_password} onChange={handleS} required /></FormGroup>
                  </FormRow>
                  <SubmitBtn type="submit" disabled={loading}>{loading ? "Creating..." : "Create Account →"}</SubmitBtn>
                </form>
              )}

              {isCompany && (
                <form onSubmit={submitCompany}>
                  <FormGroup><Label>Company Name</Label><Input name="company_name" placeholder="Sonatrach, Djezzy..." value={cForm.company_name} onChange={handleC} required /></FormGroup>
                  <FormGroup><Label>Professional Email</Label><Input type="email" name="email" placeholder="rh@company.com" value={cForm.email} onChange={handleC} required /></FormGroup>
                  <FormRow>
                    <FormGroup><Label>Phone</Label><Input name="phone" placeholder="+213..." value={cForm.phone} onChange={handleC} /></FormGroup>
                    <FormGroup><Label>Wilaya</Label><Input name="address" placeholder="Alger, Oran..." value={cForm.address} onChange={handleC} /></FormGroup>
                  </FormRow>
                  <FormRow>
                    <FormGroup><Label>Password</Label><Input type="password" name="password" placeholder="••••••••" value={cForm.password} onChange={handleC} required /></FormGroup>
                    <FormGroup><Label>Confirm</Label><Input type="password" name="confirm_password" placeholder="••••••••" value={cForm.confirm_password} onChange={handleC} required /></FormGroup>
                  </FormRow>
                  <SubmitBtn type="submit" disabled={loading}>{loading ? "Registering..." : "Register Company →"}</SubmitBtn>
                </form>
              )}

              <FooterText>Already have an account? <Link to="/login">Sign in</Link></FooterText>
            </Card>
          </Center>
        </Above>
      </PageBg>
    </ThemeProvider>
  );
}
