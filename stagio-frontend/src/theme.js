// src/theme.js
// This file contains the FULL theme for the entire app.
// Every page imports from here — change colors here = changes everywhere.

import { createGlobalStyle, keyframes } from "styled-components";

// ─── ANIMATIONS (shared across all pages) ────────────────────────────────────

export const fadeUp = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
`;

export const fadeIn = keyframes`
  from { opacity: 0; }
  to   { opacity: 1; }
`;

export const pulse = keyframes`
  0%, 100% { opacity: 0.5; }
  50%       { opacity: 1; }
`;

export const float = keyframes`
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.05); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
`;

// ─── DARK THEME ───────────────────────────────────────────────────────────────

export const darkTheme = {
  // backgrounds
  bg:           "#0e0818",
  bgNav:        "rgba(20,8,35,0.75)",
  bgCard:       "rgba(30,10,55,0.55)",
  bgCardHover:  "rgba(40,12,75,0.7)",
  bgStat:       "rgba(123,47,255,0.08)",
  bgStatHover:  "rgba(123,47,255,0.14)",
  bgInput:      "rgba(123,47,255,0.06)",
  bgBtn:        "rgba(123,47,255,0.1)",
  bgTag:        "rgba(123,47,255,0.1)",

  // blobs
  blob1: "rgba(180,40,255,0.2)",
  blob2: "rgba(255,50,180,0.1)",
  blob3: "rgba(123,47,255,0.1)",

  // borders
  border:       "rgba(123,47,255,0.12)",
  borderHover:  "rgba(255,58,170,0.3)",
  borderNav:    "rgba(180,100,255,0.12)",
  borderInput:  "rgba(123,47,255,0.2)",
  borderBtn:    "rgba(123,47,255,0.25)",
  borderTag:    "rgba(123,47,255,0.18)",

  // text
  text:         "#e8d5ff",
  textSub:      "rgba(200,160,255,0.5)",
  textMuted:    "rgba(200,160,255,0.3)",
  textFaint:    "rgba(200,160,255,0.15)",

  // accents
  accent:       "#7b2fff",
  accentPink:   "#ff3aaa",
  accentGlow:   "rgba(123,47,255,0.4)",
  accentGrad:   "linear-gradient(135deg, #7b2fff, #c8005a)",

  // shadows
  cardShadow:   "0 8px 32px rgba(123,47,255,0.15)",
  navShadow:    "none",
};

// ─── LIGHT THEME ─────────────────────────────────────────────────────────────

export const lightTheme = {
  // backgrounds
  bg:           "#f3eeff",
  bgNav:        "rgba(255,255,255,0.65)",
  bgCard:       "rgba(255,255,255,0.5)",
  bgCardHover:  "rgba(255,255,255,0.82)",
  bgStat:       "rgba(255,255,255,0.55)",
  bgStatHover:  "rgba(255,255,255,0.85)",
  bgInput:      "rgba(255,255,255,0.7)",
  bgBtn:        "rgba(123,47,255,0.08)",
  bgTag:        "rgba(100,20,200,0.06)",

  // blobs
  blob1: "rgba(160,60,240,0.12)",
  blob2: "rgba(220,60,160,0.08)",
  blob3: "rgba(123,47,255,0.07)",

  // borders
  border:       "rgba(123,47,255,0.1)",
  borderHover:  "rgba(255,58,170,0.25)",
  borderNav:    "rgba(140,60,200,0.1)",
  borderInput:  "rgba(123,47,255,0.2)",
  borderBtn:    "rgba(123,47,255,0.2)",
  borderTag:    "rgba(100,20,200,0.12)",

  // text
  text:         "#1a0530",
  textSub:      "rgba(80,20,140,0.6)",
  textMuted:    "rgba(80,20,140,0.35)",
  textFaint:    "rgba(80,20,140,0.2)",

  // accents
  accent:       "#7b2fff",
  accentPink:   "#ff3aaa",
  accentGlow:   "rgba(123,47,255,0.2)",
  accentGrad:   "linear-gradient(135deg, #7b2fff, #c8005a)",

  // shadows
  cardShadow:   "0 4px 24px rgba(123,47,255,0.08)",
  navShadow:    "0 1px 0 rgba(140,60,200,0.1)",
};

// ─── GLOBAL STYLES ────────────────────────────────────────────────────────────

export const GlobalStyle = createGlobalStyle`
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  html, body, #root { height: 100%; }

  body {
    background: ${({ theme }) => theme.bg};
    font-family: 'DM Sans', sans-serif;
    -webkit-font-smoothing: antialiased;
    transition: background 0.3s;
  }

  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb {
    background: ${({ theme }) => theme.border};
    border-radius: 4px;
  }
`;

// ─── SHARED LAYOUT COMPONENTS ────────────────────────────────────────────────
// Used by all dashboard pages

import styled from "styled-components";

// Full page wrapper with background blobs
export const PageBg = styled.div`
  min-height: 100vh;
  background: ${({ theme }) => theme.bg};
  position: relative;
  overflow-x: hidden;
  transition: background 0.3s;

  /* blob 1 — top right */
  &::before {
    content: '';
    position: fixed;
    width: 600px; height: 600px;
    background: radial-gradient(circle, ${({ theme }) => theme.blob1} 0%, transparent 65%);
    top: -200px; right: -150px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    animation: ${float} 20s ease-in-out infinite;
  }

  /* blob 2 — bottom left */
  &::after {
    content: '';
    position: fixed;
    width: 500px; height: 500px;
    background: radial-gradient(circle, ${({ theme }) => theme.blob2} 0%, transparent 65%);
    bottom: -150px; left: -100px;
    border-radius: 50%;
    pointer-events: none;
    z-index: 0;
    animation: ${float} 25s ease-in-out infinite reverse;
  }
`;

export const BlobMid = styled.div`
  position: fixed;
  width: 400px; height: 400px;
  background: radial-gradient(circle, ${({ theme }) => theme.blob3} 0%, transparent 65%);
  top: 40%; left: 30%;
  border-radius: 50%;
  pointer-events: none;
  z-index: 0;
  animation: ${float} 22s ease-in-out infinite 2s;
`;

export const Above = styled.div`
  position: relative;
  z-index: 1;
  max-width: 1000px;
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
`;

// ── TOP NAVBAR ──
export const Navbar = styled.nav`
  display: flex;
  align-items: stretch;
  height: 64px;
  background: ${({ theme }) => theme.bgNav};
  backdrop-filter: blur(24px);
  border-bottom: 1px solid ${({ theme }) => theme.borderNav};
  padding: 0 5vw;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: ${({ theme }) => theme.navShadow};
  margin-bottom: 24px;
`;

export const NavLogo = styled.div`
  display: flex; align-items: center; gap: 10px;
  padding-right: 28px;
  border-right: 1px solid ${({ theme }) => theme.borderNav};
  margin-right: 8px;
`;

export const NavLogoSquare = styled.div`
  width: 30px; height: 30px;
  background: ${({ theme }) => theme.accentGrad};
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700; color: #fff;
  border-radius: 8px;
  box-shadow: 0 0 14px ${({ theme }) => theme.accentGlow};
`;

export const NavLogoImage = styled.img`
  width: 34px; height: 34px;
  border-radius: 8px;
  object-fit: cover;
  box-shadow: 0 0 14px ${({ theme }) => theme.accentGlow};
`;

export const NavLogoText = styled.span`
  font-size: 16px; font-weight: 700;
  color: ${({ theme }) => theme.text};
  letter-spacing: -0.3px;
`;


export const NavTabs = styled.div`
  display: flex; align-items: stretch; flex: 1;
`;

export const NavTab = styled.button`
  display: flex; align-items: center;
  padding: 0 18px;
  font-size: 13px; font-weight: 500;
  color: ${({ $active, theme }) => $active ? theme.text : theme.textMuted};
  background: none; border: none;
  border-bottom: 2px solid ${({ $active, theme }) => $active ? theme.accent : 'transparent'};
  cursor: pointer; transition: all 0.15s;
  font-family: 'DM Sans', sans-serif;
  letter-spacing: 0.01em;

  &:hover { color: ${({ theme }) => theme.textSub}; }
`;

export const NavRight = styled.div`
  display: flex; align-items: center; gap: 10px;
  padding-left: 16px;
  border-left: 1px solid ${({ theme }) => theme.borderNav};
  margin-left: 8px;
`;

export const ThemeToggleBtn = styled.button`
  padding: 6px 14px;
  background: ${({ theme }) => theme.bgBtn};
  border: 1px solid ${({ theme }) => theme.borderBtn};
  border-radius: 20px;
  font-size: 11px; color: ${({ theme }) => theme.textSub};
  font-family: 'DM Sans', sans-serif;
  cursor: pointer; transition: all 0.2s;
  letter-spacing: 0.05em;

  &:hover { border-color: ${({ theme }) => theme.accent}; color: ${({ theme }) => theme.text}; }
`;

export const NavAvatar = styled.div`
  width: 32px; height: 32px;
  background: ${({ theme }) => theme.accentGrad};
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700; color: #fff;
  cursor: pointer;
  box-shadow: 0 0 10px ${({ theme }) => theme.accentGlow};
  overflow: hidden;
  img { width: 100%; height: 100%; object-fit: cover; }
`;

// ── HERO SECTION ──
export const Hero = styled.div`
  padding: 32px 28px 24px;
  display: flex; align-items: flex-end;
  justify-content: space-between;
  gap: 20px; flex-wrap: wrap;
`;

export const HeroLabel = styled.p`
  font-size: 9px; color: ${({ theme }) => theme.accentPink};
  letter-spacing: 0.25em; text-transform: uppercase;
  font-weight: 600; margin-bottom: 6px;
  display: flex; align-items: center; gap: 8px;

  &::before { content: ''; width: 16px; height: 1px; background: ${({ theme }) => theme.accentPink}; }
`;

export const HeroTitle = styled.h1`
  font-size: 26px; font-weight: 700;
  color: ${({ theme }) => theme.text};
  letter-spacing: -0.5px; line-height: 1.1; margin-bottom: 4px;

  span { color: ${({ theme }) => theme.accentPink}; }
`;

export const HeroSub = styled.p`
  font-size: 13px; color: ${({ theme }) => theme.textMuted};
`;

// ── STAT CARDS ROW ──
export const StatsRow = styled.div`
  display: flex; gap: 10px; flex-wrap: wrap;
`;

export const StatCard = styled.div`
  padding: 14px 18px;
  background: ${({ theme }) => theme.bgStat};
  backdrop-filter: blur(20px);
  border: 1px solid ${({ theme }) => theme.border};
  border-radius: 12px; min-width: 88px;
  transition: all 0.2s;

  &:hover {
    background: ${({ theme }) => theme.bgStatHover};
    border-color: ${({ theme }) => theme.borderHover};
  }
`;

export const StatValue = styled.p`
  font-size: 26px; font-weight: 700;
  color: ${({ $pink, theme }) => $pink ? theme.accentPink : theme.text};
  letter-spacing: -1px; line-height: 1;
`;

export const StatLabel = styled.p`
  font-size: 10px; color: ${({ theme }) => theme.textMuted};
  text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px;
`;

// ── CONTENT AREA ──
export const Content = styled.div`
  padding: 0 28px 32px;
  animation: ${fadeUp} 0.4s ease;
`;

export const SectionRow = styled.div`
  display: flex; align-items: center;
  justify-content: space-between; margin-bottom: 14px;
`;

export const SectionTitle = styled.h2`
  font-size: 11px; font-weight: 600;
  color: ${({ theme }) => theme.textMuted};
  letter-spacing: 0.15em; text-transform: uppercase;
`;

export const SeeAllBtn = styled.button`
  font-size: 11px; color: ${({ theme }) => theme.textMuted};
  background: none; border: none; cursor: pointer;
  font-family: 'DM Sans', sans-serif; transition: color 0.15s;
  &:hover { color: ${({ theme }) => theme.accentPink}; }
`;

// ── GLASS CARDS ──
export const GlassCard = styled.div`
  background: ${({ theme }) => theme.bgCard};
  backdrop-filter: blur(24px);
  border: 1px solid ${({ theme }) => theme.border};
  border-radius: 16px; padding: 20px;
  position: relative; overflow: hidden;
  transition: all 0.2s;
  box-shadow: ${({ theme }) => theme.cardShadow};

  &::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, ${({ theme }) => theme.border}, transparent);
  }

  &:hover {
    background: ${({ theme }) => theme.bgCardHover};
    border-color: ${({ theme }) => theme.borderHover};
    transform: translateY(-2px);
  }
`;

export const CardGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 14px;
`;

// ── TAGS ──
export const Tag = styled.span`
  font-size: 10px; padding: 3px 9px;
  background: ${({ theme }) => theme.bgTag};
  border: 1px solid ${({ theme }) => theme.borderTag};
  border-radius: 20px;
  color: ${({ theme }) => theme.textSub};
  letter-spacing: 0.03em;
`;

export const TagsRow = styled.div`
  display: flex; gap: 5px; flex-wrap: wrap;
`;

// ── BUTTONS ──
export const PrimaryButton = styled.button`
  padding: 10px 22px;
  background: ${({ theme }) => theme.accentGrad};
  border: none; border-radius: 10px;
  color: #fff; font-family: 'DM Sans', sans-serif;
  font-size: 13px; font-weight: 600; cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
  box-shadow: 0 4px 16px ${({ theme }) => theme.accentGlow};
  letter-spacing: 0.02em;

  &:hover:not(:disabled) { opacity: 0.88; transform: translateY(-1px); }
  &:active:not(:disabled) { transform: translateY(0); }
  &:disabled { opacity: 0.4; cursor: not-allowed; }
`;

export const GhostButton = styled.button`
  padding: 8px 16px;
  background: ${({ theme }) => theme.bgBtn};
  border: 1px solid ${({ theme }) => theme.borderBtn};
  border-radius: 9px;
  color: ${({ theme }) => theme.textSub};
  font-family: 'DM Sans', sans-serif;
  font-size: 12px; font-weight: 500; cursor: pointer;
  transition: all 0.15s;

  &:hover { border-color: ${({ theme }) => theme.accent}; color: ${({ theme }) => theme.text}; }
`;

export const DangerButton = styled(GhostButton)`
  border-color: rgba(255,58,100,0.2);
  color: rgba(255,80,100,0.7);
  &:hover { background: rgba(255,58,100,0.1); border-color: rgba(255,58,100,0.4); color: #ff5064; }
`;

export const SuccessButton = styled(GhostButton)`
  border-color: rgba(100,255,180,0.2);
  color: rgba(100,220,160,0.7);
  &:hover { background: rgba(100,255,180,0.08); border-color: rgba(100,255,180,0.35); color: #64ffb4; }
`;

// ── FORM ELEMENTS ──
export const FormCard = styled(GlassCard)`
  max-width: 560px;
  &:hover { transform: none; }
`;

export const FormGroup = styled.div`margin-bottom: 18px;`;

export const FormRow = styled.div`
  display: grid; grid-template-columns: 1fr 1fr; gap: 14px;
  @media (max-width: 480px) { grid-template-columns: 1fr; }
`;

export const Label = styled.label`
  display: block; font-size: 11px; font-weight: 500;
  color: ${({ theme }) => theme.textSub};
  letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 7px;
`;

export const Input = styled.input`
  width: 100%; padding: 11px 14px;
  background: ${({ theme }) => theme.bgInput};
  border: 1px solid ${({ theme }) => theme.borderInput};
  border-radius: 10px;
  color: ${({ theme }) => theme.text};
  font-family: 'DM Sans', sans-serif; font-size: 13px; outline: none;
  transition: border-color 0.2s, background 0.2s;

  &::placeholder { color: ${({ theme }) => theme.textFaint}; }
  &:focus {
    border-color: ${({ theme }) => theme.accent};
    background: rgba(123,47,255,0.08);
  }
`;

export const SuccessMsg = styled.div`
  background: rgba(100,255,180,0.07);
  border: 1px solid rgba(100,255,180,0.2);
  border-radius: 10px; padding: 11px 14px;
  color: #64ffb4; font-size: 13px; margin-bottom: 16px;
`;

export const ErrorMsg = styled.div`
  background: rgba(255,58,100,0.08);
  border: 1px solid rgba(255,58,100,0.2);
  border-radius: 10px; padding: 11px 14px;
  color: #ff8099; font-size: 13px; margin-bottom: 16px;
`;

// ── STATUS BADGE ──
export const StatusBadge = styled.span`
  padding: 3px 10px; border-radius: 20px;
  font-size: 11px; font-weight: 500;
  background: ${({ $status }) =>
    $status === "accepted" ? "rgba(100,255,180,0.08)" :
    $status === "rejected" ? "rgba(255,58,100,0.08)" :
    "rgba(123,47,255,0.08)"};
  color: ${({ $status }) =>
    $status === "accepted" ? "#64ffb4" :
    $status === "rejected" ? "#ff5064" :
    "#c8a0ff"};
  border: 1px solid ${({ $status }) =>
    $status === "accepted" ? "rgba(100,255,180,0.2)" :
    $status === "rejected" ? "rgba(255,58,100,0.2)" :
    "rgba(123,47,255,0.2)"};
`;

export const EmptyState = styled.div`
  text-align: center; padding: 48px 20px;
  color: ${({ theme }) => theme.textFaint}; font-size: 13px;
  p:first-child { font-size: 32px; margin-bottom: 10px; }
`;
