import React, { useState } from 'react';
import styled, { ThemeProvider } from 'styled-components';
import { useNavigate } from 'react-router-dom';
import {
  darkTheme, lightTheme, GlobalStyle, PageBg, BlobMid, Above,
  Navbar, NavLogo, NavLogoSquare, NavLogoImage, NavLogoText, NavRight, ThemeToggleBtn,
  PrimaryButton, GhostButton, GlassCard, fadeUp
} from '../theme';
import { keyframes } from 'styled-components';

// ── New Animations ──
const slideInLeft = keyframes`
  from { opacity: 0; transform: translateX(-50px); }
  to   { opacity: 1; transform: translateX(0); }
`;

const slideInRight = keyframes`
  from { opacity: 0; transform: translateX(50px); }
  to   { opacity: 1; transform: translateX(0); }
`;

const zoomIn = keyframes`
  from { opacity: 0; transform: scale(0.9); }
  to   { opacity: 1; transform: scale(1); }
`;

const floatCrazy = keyframes`
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  25% { transform: translateY(-10px) rotate(2deg); }
  75% { transform: translateY(10px) rotate(-2deg); }
`;

const driftLight1 = keyframes`
  0%, 100% { transform: translate(0, 0) scale(1) rotate(0deg); opacity: 0.4; }
  33% { transform: translate(30vw, 20vh) scale(1.5) rotate(45deg); opacity: 0.8; }
  66% { transform: translate(-10vw, 40vh) scale(0.8) rotate(90deg); opacity: 0.3; }
`;

const driftLight2 = keyframes`
  0%, 100% { transform: translate(0, 0) scale(1) rotate(0deg); opacity: 0.4; }
  33% { transform: translate(-30vw, -20vh) scale(1.3) rotate(-45deg); opacity: 0.7; }
  66% { transform: translate(20vw, 10vh) scale(0.9) rotate(-90deg); opacity: 0.2; }
`;

const textGlow = keyframes`
  0%, 100% { text-shadow: 0 0 10px rgba(123,47,255,0.2), 0 0 20px rgba(123,47,255,0.1); }
  50% { text-shadow: 0 0 20px rgba(123,47,255,0.6), 0 0 40px rgba(255,58,170,0.4); }
`;

const GlowingOrb = styled.div`
  position: fixed;
  border-radius: 50%;
  filter: blur(120px);
  z-index: 0;
  pointer-events: none;
`;

const Orb1 = styled(GlowingOrb)`
  top: 10%; left: 10%; width: 400px; height: 400px; background: rgba(255, 58, 170, 0.4);
  animation: ${driftLight1} 15s infinite alternate ease-in-out;
`;

const Orb2 = styled(GlowingOrb)`
  bottom: 20%; right: 10%; width: 500px; height: 500px; background: rgba(123, 47, 255, 0.4);
  animation: ${driftLight2} 20s infinite alternate ease-in-out;
`;

const Orb3 = styled(GlowingOrb)`
  top: 50%; left: 50%; width: 600px; height: 600px; background: rgba(76, 255, 154, 0.2);
  animation: ${driftLight1} 25s infinite alternate-reverse ease-in-out;
`;

// ── Additional styled bits for Landing Page ──
const LandingContainer = styled.div`
  width: 100%;
  padding: 0 5vw;
  position: relative;
  z-index: 1;
`;

const LandingHero = styled.div`
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  text-align: center; padding: 160px 20px 120px;
  animation: ${zoomIn} 0.8s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  width: 100%;
`;

const Badge = styled.div`
  background: ${({ theme }) => theme.bgBtn};
  border: 1px solid ${({ theme }) => theme.borderBtn};
  border-radius: 30px; padding: 12px 24px;
  font-size: 16px; font-weight: 700; color: ${({ theme }) => theme.accentPink};
  letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 30px;
  animation: ${slideInLeft} 1s ease, ${textGlow} 3s infinite;
  box-shadow: 0 0 20px rgba(255,58,170,0.3);
`;

const Title = styled.h1`
  font-size: 100px; font-weight: 800; color: ${({ theme }) => theme.text};
  line-height: 1.1; margin-bottom: 30px;
  letter-spacing: -3px;
  animation: ${zoomIn} 1s ease, ${textGlow} 4s infinite alternate;
  width: 100%;
  span {
    background: ${({ theme }) => theme.accentGrad};
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  @media (max-width: 1200px) { font-size: 80px; }
  @media (max-width: 768px) { font-size: 50px; }
`;

const Subtitle = styled.p`
  font-size: 28px; color: ${({ theme }) => theme.textMuted};
  line-height: 1.6; margin-bottom: 60px; max-width: 1200px;
  animation: ${fadeUp} 1.2s ease;
  font-weight: 400;
`;

const ActionButtons = styled.div`
  display: flex; gap: 20px; flex-wrap: wrap; justify-content: center;
  animation: ${fadeUp} 1.4s ease;
`;

// ── Zig-Zag Section Styles ──
const ZigZagSection = styled.section`
  display: flex;
  align-items: center;
  gap: 100px;
  padding: 140px 0;
  flex-direction: ${({ $reverse }) => $reverse ? 'row-reverse' : 'row'};
  width: 100%;
  
  @media (max-width: 900px) {
    flex-direction: column;
    text-align: center;
    gap: 40px;
  }
`;

const ZigZagContent = styled.div`
  flex: 1;
  animation: ${({ $reverse }) => $reverse ? slideInRight : slideInLeft} 1s ease;
`;

const ZigZagImageWrapper = styled.div`
  flex: 1;
  position: relative;
  animation: ${zoomIn} 1s ease;
  transition: transform 0.3s;
  &:hover { transform: scale(1.03); }
  
  &::before {
    content: '';
    position: absolute;
    top: -20px;
    left: -20px;
    right: 20px;
    bottom: 20px;
    border-radius: 24px;
    border: 2px solid ${({ theme }) => theme.borderHover};
    z-index: -1;
    transform: ${({ $reverse }) => $reverse ? 'translate(40px, 40px)' : 'none'};
  }
`;

const ZigZagImage = styled.img`
  width: 100%;
  border-radius: 30px;
  box-shadow: 0 20px 60px rgba(123,47,255,0.3);
  object-fit: cover;
  min-height: 600px;
  animation: ${floatCrazy} 6s ease-in-out infinite;
`;

const SectionPretitle = styled.p`
  font-size: 18px; font-weight: 700; color: ${({ theme }) => theme.accentPink};
  letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 16px;
  animation: ${textGlow} 3s infinite alternate;
`;

const SectionTitle = styled.h2`
  font-size: 64px; font-weight: 800; color: ${({ theme }) => theme.text};
  line-height: 1.1; margin-bottom: 24px; letter-spacing: -2px;
`;

const SectionDesc = styled.p`
  font-size: 24px; color: ${({ theme }) => theme.textSub};
  line-height: 1.7; margin-bottom: 40px;
`;

const FeatureList = styled.ul`
  list-style: none; padding: 0; margin: 0;
  li {
    font-size: 22px; color: ${({ theme }) => theme.text};
    margin-bottom: 16px; display: flex; align-items: center; gap: 14px;
    font-weight: 500;
    &::before { content: '✓'; color: #4cff9a; font-weight: bold; font-size: 26px; }
  }
`;

const CallToAction = styled.div`
  text-align: center;
  padding: 160px 20px;
  margin-top: 80px;
  background: ${({ theme }) => theme.bgCard};
  border-top: 1px solid ${({ theme }) => theme.border};
  position: relative;
  overflow: hidden;
  animation: ${zoomIn} 1.5s ease;
`;

const CTABackgroundImage = styled.img`
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  width: 100%; height: 100%;
  object-fit: cover;
  opacity: 0.15;
  z-index: 0;
  pointer-events: none;
`;

const CTAContent = styled.div`
  position: relative;
  z-index: 1;
`;

export default function LandingPage() {
  const [isDark, setIsDark] = useState(true);
  const theme = isDark ? darkTheme : lightTheme;
  const navigate = useNavigate();

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <PageBg>
        <BlobMid />
        {/* Wild Background Animations */}
        <Orb1 />
        <Orb2 />
        <Orb3 />
        
        {/* Navbar is OUTSIDE Above container so it's full width */}
        <Navbar>
          <NavLogo>
            <NavLogoImage src="/logo.png" alt="Stag.io Logo" />
            <NavLogoText>STAG.IO</NavLogoText>
          </NavLogo>
          <div style={{ flex: 1 }} />
          <NavRight>
            <ThemeToggleBtn onClick={() => setIsDark(p => !p)}>
              {isDark ? "☀ Light" : "🌙 Dark"}
            </ThemeToggleBtn>
            <GhostButton onClick={() => navigate('/login')}>Sign In</GhostButton>
            <PrimaryButton onClick={() => navigate('/register')} style={{ padding: '8px 16px', fontSize: '12px' }}>
              Register Free
            </PrimaryButton>
          </NavRight>
        </Navbar>

        <LandingContainer>
          <LandingHero>
            <Badge>Algeria's #1 Internship Portal</Badge>
            <Title>Launch Your Career.<br />Find the <span>Perfect Internship</span>.</Title>
            <Subtitle>
              Connect with top companies, build a stunning professional profile, and fast-track your university placement requirements in a single click.
            </Subtitle>
            <ActionButtons>
              {/* As requested: Get Started -> Login */}
              <PrimaryButton onClick={() => navigate('/login')} style={{ padding: '24px 56px', fontSize: '22px', borderRadius: '16px' }}>
                Get Started
              </PrimaryButton>
            </ActionButtons>
          </LandingHero>

          {/* Zig-Zag Section 1: Text Left, Image Right */}
          <ZigZagSection>
            <ZigZagContent>
              <SectionPretitle>For Students</SectionPretitle>
              <SectionTitle>Stand Out From The Crowd.</SectionTitle>
              <SectionDesc>
                Say goodbye to boring CVs. Create a dynamic profile that showcases your skills, links your GitHub and Portfolio, and lets companies find YOU.
              </SectionDesc>
              <FeatureList>
                <li>One-click applications to top tier offers.</li>
                <li>Track your application status in real-time.</li>
                <li>Automated PDF internship agreements.</li>
              </FeatureList>
            </ZigZagContent>
            <ZigZagImageWrapper>
              <ZigZagImage src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" alt="Students collaborating on a laptop" />
            </ZigZagImageWrapper>
          </ZigZagSection>

          {/* Zig-Zag Section 2: Image Left, Text Right ($reverse=true) */}
          <ZigZagSection $reverse>
            <ZigZagContent $reverse>
              <SectionPretitle>For Companies</SectionPretitle>
              <SectionTitle>Hire The Top 1% Of Talent.</SectionTitle>
              <SectionDesc>
                Filter through verified university students with exact skill matches. Validate internship agreements instantly and manage all your offers from a beautiful dashboard.
              </SectionDesc>
              <FeatureList>
                <li>Post internship offers in seconds.</li>
                <li>Review comprehensive student profiles.</li>
                <li>Accept and reject with automatic notifications.</li>
              </FeatureList>
            </ZigZagContent>
            <ZigZagImageWrapper $reverse>
              <ZigZagImage src="https://images.unsplash.com/photo-1552664730-d307ca884978?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80" alt="Modern corporate office" />
            </ZigZagImageWrapper>
          </ZigZagSection>

          {/* Zig-Zag Section 3: Text Left, Image Right */}
          <ZigZagSection>
            <ZigZagContent>
              <SectionPretitle>Seamless Process</SectionPretitle>
              <SectionTitle>No More Paperwork Hassle.</SectionTitle>
              <SectionDesc>
                We've digitized the entire university internship agreement process. Once accepted, your PDF agreement is automatically generated, formatted, and ready for signatures.
              </SectionDesc>
              <PrimaryButton onClick={() => navigate('/register')} style={{ marginTop: '30px', padding: '20px 40px', fontSize: '20px' }}>Join the Platform Today</PrimaryButton>
            </ZigZagContent>
            <ZigZagImageWrapper>
              <ZigZagImage src="/logo.png" alt="Platform Logo" style={{ objectFit: 'contain', padding: '40px', background: 'rgba(10, 5, 20, 0.4)' }} />
            </ZigZagImageWrapper>
          </ZigZagSection>
        </LandingContainer>

        <CallToAction>
          <CTABackgroundImage src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80" alt="Students cheering" />
          <CTAContent>
            <Title style={{ fontSize: '80px', animation: 'none' }}>Ready to get started?</Title>
            <Subtitle style={{ margin: '0 auto 50px', fontSize: '28px', maxWidth: '800px' }}>Join thousands of students and hundreds of companies actively hiring today.</Subtitle>
            <PrimaryButton onClick={() => navigate('/login')} style={{ padding: '24px 64px', fontSize: '24px', borderRadius: '20px' }}>
              Get Started Now
            </PrimaryButton>
          </CTAContent>
        </CallToAction>
        
      </PageBg>
    </ThemeProvider>
  );
}
