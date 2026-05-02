// src/pages/student/StudentDashboard.jsx
import React, { useState, useEffect, useRef } from "react";
import styled, { ThemeProvider } from "styled-components";
import {
  darkTheme, lightTheme, GlobalStyle, PageBg, BlobMid, Above,
  Navbar, NavLogo, NavLogoSquare, NavLogoImage, NavLogoText, NavTabs, NavTab,
  NavRight, ThemeToggleBtn, NavAvatar,
  Hero, HeroLabel, HeroTitle, HeroSub,
  StatsRow, StatCard, StatValue, StatLabel,
  Content, SectionRow, SectionTitle, SeeAllBtn,
  GlassCard, CardGrid, Tag, TagsRow,
  PrimaryButton, GhostButton,
  FormCard, FormGroup, FormRow, Label, Input,
  SuccessMsg, ErrorMsg, EmptyState, fadeUp
} from "../../theme";
import { useAuth } from "../../context/AuthContext";
import api from "../../api/axios";
import { getOffers, applyToOffer, getMyApplications, getMySkills, getAllSkills, addSkill, removeSkill, getNotifications, markNotifRead, downloadAgreement } from "../../api/studentApi";

// ── Extra styled bits ────────────────────────────────────────────────────────
const OfferBanner = styled.div`
  width:100%;height:140px;border-radius:12px 12px 0 0;
  background:${({ theme }) => theme.bgBtn};
  overflow:hidden;margin:-20px -20px 16px -20px;width:calc(100% + 40px);
  position:relative;
  img{width:100%;height:100%;object-fit:cover;}
  .fallback{
    width:100%;height:100%;display:flex;align-items:center;justify-content:center;
    background:linear-gradient(135deg,${({ theme }) => theme.bgBtn},${({ theme }) => theme.bgCard});
    font-size:40px;
  }
`;
const OfferCompany = styled.p`font-size:11px;font-weight:700;color:${({ theme }) => theme.accentPink};letter-spacing:0.08em;text-transform:uppercase;margin-bottom:6px;display:flex;align-items:center;gap:7px;`;
const CompanyLogo = styled.img`width:22px;height:22px;border-radius:6px;object-fit:cover;border:1px solid ${({ theme }) => theme.border};`;
const OfferTitle = styled.h3`font-size:16px;font-weight:700;color:${({ theme }) => theme.text};line-height:1.35;margin-bottom:8px;`;
const OfferMeta = styled.p`font-size:12px;color:${({ theme }) => theme.textMuted};margin-bottom:12px;`;
const ApplyBtn = styled.button`
  width:100%;padding:11px;
  background:${({ theme }) => theme.bgBtn};
  border:1px solid ${({ theme }) => theme.borderBtn};
  border-radius:10px;font-size:13px;
  color:${({ theme }) => theme.textSub};
  font-family:'DM Sans',sans-serif;cursor:pointer;font-weight:600;
  transition:all 0.22s;
  &:hover{background:${({ theme }) => theme.accentGrad};border-color:transparent;color:#fff;box-shadow:0 4px 18px ${({ theme }) => theme.accentGlow};}
  &:disabled{opacity:0.4;cursor:not-allowed;}
`;
const ProfileCard = styled(GlassCard)`display:flex;gap:18px;align-items:flex-start;flex-wrap:wrap;&:hover{transform:none;}`;
const BigAvatar = styled.div`
  width:64px;height:64px;border-radius:50%;
  background:${({ theme }) => theme.accentGrad};
  display:flex;align-items:center;justify-content:center;
  font-size:22px;font-weight:700;color:#fff;flex-shrink:0;
  box-shadow:0 0 20px ${({ theme }) => theme.accentGlow};
  overflow:hidden;
  img{width:100%;height:100%;object-fit:cover;}
`;
const ProfileInfo = styled.div`flex:1;h3{font-size:18px;font-weight:700;color:${({ theme }) => theme.text};margin-bottom:2px;}p{font-size:13px;color:${({ theme }) => theme.textMuted};margin-bottom:10px;}`;
const LastActiveBadge = styled.span`
  display:inline-flex;align-items:center;gap:5px;
  font-size:11px;color:${({ theme }) => theme.textFaint};
  &::before{content:'';width:7px;height:7px;border-radius:50%;background:#4cff9a;display:inline-block;box-shadow:0 0 6px #4cff9a;}
`;
const SaveBtn = styled(PrimaryButton)`padding:10px 28px;`;
const SearchBar = styled.div`display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap;`;
const SearchInput = styled(Input)`flex:1;min-width:180px;`;
const FilterSelect = styled.select`
  padding:11px 14px;
  background:${({ theme }) => theme.bgInput};
  border:1px solid ${({ theme }) => theme.borderInput};
  border-radius:10px;color:${({ theme }) => theme.text};
  font-family:'DM Sans',sans-serif;font-size:13px;outline:none;
  cursor:pointer;
  option{background:#1a0a2e;}
`;
const AppRow = styled.div`display:flex;align-items:center;gap:12px;padding:16px 0;border-bottom:1px solid ${({ theme }) => theme.border};&:last-child{border-bottom:none;}flex-wrap:wrap;`;
const AppInfo = styled.div`flex:1;p{font-size:14px;font-weight:600;color:${({ theme }) => theme.text};}span{font-size:12px;color:${({ theme }) => theme.textMuted};}`;
const StatusBadge = styled.span`
  padding:4px 12px;border-radius:20px;font-size:11px;font-weight:600;
  background:${({ $s }) => $s === "validated" ? "rgba(76,255,154,0.10)" : $s === "rejected" ? "rgba(255,58,100,0.10)" : "rgba(123,47,255,0.10)"};
  color:${({ $s }) => $s === "validated" ? "#4cff9a" : $s === "rejected" ? "#ff5064" : "#c8a0ff"};
  border:1px solid ${({ $s }) => $s === "validated" ? "rgba(76,255,154,0.25)" : $s === "rejected" ? "rgba(255,58,100,0.25)" : "rgba(123,47,255,0.25)"};
`;
const PrivacyBtn = styled.button`
  padding:4px 10px;border-radius:20px;font-size:11px;font-weight:600;cursor:pointer;
  background:${({ $on, theme }) => $on ? "rgba(76,255,154,0.12)" : theme.bgBtn};
  color:${({ $on }) => $on ? "#4cff9a" : "#888"};
  border:1px solid ${({ $on }) => $on ? "rgba(76,255,154,0.3)" : "rgba(255,255,255,0.08)"};
  font-family:'DM Sans',sans-serif;transition:all 0.2s;
  &:hover{border-color:${({ theme }) => theme.accent};color:${({ theme }) => theme.text};}
`;
const NotifDot = styled.span`width:8px;height:8px;border-radius:50%;background:${({ theme }) => theme.accentPink};display:inline-block;margin-right:6px;`;
const SkillPill = styled.span`
  display:inline-flex;align-items:center;gap:6px;
  padding:5px 12px;
  background:${({ theme }) => theme.bgTag};
  border:1px solid ${({ theme }) => theme.borderTag};
  border-radius:20px;font-size:12px;color:${({ theme }) => theme.textSub};
  button{background:none;border:none;color:${({ theme }) => theme.accentPink};cursor:pointer;font-size:14px;line-height:1;padding:0;}
`;
const BioTextarea = styled.textarea`
  width:100%;min-height:120px;resize:vertical;
  padding:14px;box-sizing:border-box;
  background:${({ theme }) => theme.bgInput};
  border:1px solid ${({ theme }) => theme.borderInput};
  border-radius:12px;color:${({ theme }) => theme.text};
  font-family:'DM Sans',sans-serif;font-size:14px;line-height:1.6;
  outline:none;transition:border 0.2s;
  &:focus{border-color:${({ theme }) => theme.accent};}
  &::placeholder{color:${({ theme }) => theme.textFaint};}
`;

// ── Mock fallbacks (used when backend not ready) ─────────────────────────────
const MOCK_OFFERS = [
  { id: 1, title: "Frontend Developer Intern", company_name: "Djezzy", wilaya: "Alger", duration: "2 months", skills: [{ name: "React" }, { name: "CSS" }] },
  { id: 2, title: "Backend Python Intern", company_name: "Sonatrach", wilaya: "Oran", duration: "3 months", skills: [{ name: "Python" }, { name: "Django" }] },
  { id: 3, title: "Full-Stack Web Developer", company_name: "Mobilis", wilaya: "Alger", duration: "6 months", skills: [{ name: "React" }, { name: "Node.js" }] },
];
const MOCK_SKILLS = [
  { id: 1, name: "React" }, { id: 2, name: "Python" }, { id: 3, name: "Django" },
  { id: 4, name: "Node.js" }, { id: 5, name: "CSS" }, { id: 6, name: "Java" },
  { id: 7, name: "JavaScript" }, { id: 8, name: "Vue.js" }, { id: 9, name: "FastAPI" },
];

const TABS = ["Home", "Internships", "Applications", "Skills", "Notifications"];

export default function StudentDashboard() {
  const { user, logout } = useAuth();
  const [isDark, setIsDark] = useState(true);
  const [tab, setTab] = useState("Home");
  const [profile, setProfile] = useState(null);
  const [offers, setOffers] = useState(MOCK_OFFERS);
  const [applications, setApplications] = useState([]);
  const [mySkills, setMySkills] = useState([]);
  const [allSkills, setAllSkills] = useState(MOCK_SKILLS);
  const [notifs, setNotifs] = useState([]);
  const [search, setSearch] = useState("");
  const [filterWilaya, setFilterWilaya] = useState("");
  const [applying, setApplying] = useState(null);
  const [applyMsg, setApplyMsg] = useState("");
  const theme = isDark ? darkTheme : lightTheme;

  // ── Fetch data on mount ──
  useEffect(() => {
    // Profile
    api.get("/api/user/me/student/").then(r => setProfile(r.data)).catch(() => { });
    // Offers — use real API, fallback to mock
    getOffers().then(r => setOffers(r.data)).catch(() => setOffers(MOCK_OFFERS));
    // My applications
    getMyApplications().then(r => setApplications(r.data)).catch(() => setApplications([]));
    // My skills
    getMySkills().then(r => setMySkills(r.data)).catch(() => setMySkills([]));
    // All available skills
    getAllSkills().then(r => setAllSkills(r.data)).catch(() => setAllSkills(MOCK_SKILLS));
    // Notifications
    getNotifications().then(r => setNotifs(r.data)).catch(() => setNotifs([]));
  }, []);

  // ── Re-fetch offers when filters change ──
  useEffect(() => {
    getOffers({ search, wilaya: filterWilaya })
      .then(r => setOffers(r.data))
      .catch(() => {
        // fallback: filter mock data locally
        setOffers(MOCK_OFFERS.filter(o => {
          const matchSearch = !search || o.title.toLowerCase().includes(search.toLowerCase()) || o.company_name.toLowerCase().includes(search.toLowerCase());
          const matchWilaya = !filterWilaya || o.wilaya.toLowerCase().includes(filterWilaya.toLowerCase());
          return matchSearch && matchWilaya;
        }));
      });
  }, [search, filterWilaya]);

  // ── Image URL Helper ──
  const getImageUrl = (path) => {
    if (!path) return '';
    return path.startsWith('http') ? path : `http://127.0.0.1:8000${path}`;
  };

  const initials = () => {
    if (profile?.full_name) return profile.full_name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);
    const f = user?.first_name?.[0] || ""; const l = user?.last_name?.[0] || "";
    return (f + l).toUpperCase() || user?.email?.[0]?.toUpperCase() || "S";
  };
  const fullName = profile?.full_name || [user?.first_name, user?.last_name].filter(Boolean).join(" ") || user?.email;
  const unread = notifs.filter(n => !n.is_read).length;

  // ── Last active helper ──
  const lastActive = (ts) => {
    if (!ts) return null;
    const diff = Math.floor((Date.now() - new Date(ts)) / 1000);
    if (diff < 60) return "Active just now";
    if (diff < 3600) return `Active ${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `Active ${Math.floor(diff / 3600)}h ago`;
    if (diff < 604800) return `Active ${Math.floor(diff / 86400)}d ago`;
    return `Active ${Math.floor(diff / 604800)}w ago`;
  };
  const lastActiveStr = lastActive(profile?.last_seen);

  // ── Apply to offer ──
  const handleApply = async (offerId) => {
    setApplying(offerId);
    try {
      await applyToOffer(offerId);
      setApplyMsg("Application sent successfully!");
      const r = await getMyApplications(); setApplications(r.data);
      setTimeout(() => setApplyMsg(""), 3000);
    } catch (err) {
      setApplyMsg(err.response?.data?.detail || "Already applied or error occurred.");
      setTimeout(() => setApplyMsg(""), 3000);
    } finally { setApplying(null); }
  };

  // ── Add/remove skill ──
  const handleAddSkill = async (skillId) => {
    try {
      await addSkill(skillId);
      const r = await getMySkills(); setMySkills(r.data);
    } catch (err) { console.error(err); }
  };

  const handleRemoveSkill = async (skillId) => {
    try {
      await removeSkill(skillId);
      const r = await getMySkills(); setMySkills(r.data);
    } catch (err) { console.error(err); }
  };

  // ── Mark notification read ──
  const handleMarkRead = async (id) => {
    try {
      await markNotifRead(id);
      setNotifs(p => p.map(n => n.id === id ? { ...n, is_read: true } : n));
    } catch (err) { console.error(err); }
  };

  // ── Download agreement PDF ──
  const handleDownload = async (appId) => {
    try {
      const res = await downloadAgreement(appId);
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement("a"); a.href = url;
      a.download = `agreement_${appId}.pdf`; a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) { alert("Agreement not available yet."); }
  };

  const alreadyApplied = (offerId) => applications.some(a => a.offer === offerId || a.offer_id === offerId);

  // ── Privacy toggle ──
  const handlePrivacyToggle = async (appId, current) => {
    const next = current === 'public' ? 'private' : 'public';
    try {
      await api.patch(`/api/student/applications/${appId}/`, { visibility: next });
      setApplications(p => p.map(a => a.id === appId ? { ...a, visibility: next } : a));
    } catch { /* silently fail if backend not ready yet */ }
  };

  // ── Offer card renderer (shared between dashboard + internships tab) ──
  const OfferCard = ({ o }) => (
    <GlassCard key={o.id} style={{ padding: 0, overflow: 'hidden' }}>
      <OfferBanner>
        {o.cover_image || o.company_logo
          ? <img src={getImageUrl(o.cover_image || o.company_logo)} alt="offer" />
          : <div className="fallback">🎓</div>
        }
      </OfferBanner>
      <div style={{ padding: '0 20px 20px' }}>
        <OfferCompany>
          {o.company_logo && <CompanyLogo src={getImageUrl(o.company_logo)} alt={o.company_name} />}
          {o.company_name || o.company}
        </OfferCompany>
        <OfferTitle>{o.title}</OfferTitle>
        <OfferMeta>📍 {o.wilaya || o.location} · ⏱ {o.duration}</OfferMeta>
        <TagsRow style={{ marginBottom: "14px" }}>
          {(o.skills || []).map((s, i) => <Tag key={i}>{s.name || s}</Tag>)}
        </TagsRow>
        <ApplyBtn
          onClick={() => handleApply(o.id)}
          disabled={applying === o.id || alreadyApplied(o.id)}
        >
          {applying === o.id ? "Applying..." : alreadyApplied(o.id) ? "✓ Applied" : "Apply Now →"}
        </ApplyBtn>
      </div>
    </GlassCard>
  );

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <PageBg>
        <BlobMid />
        <Navbar>
            <NavLogo>
              <NavLogoImage src="/logo.png" alt="Stag.io Logo" />
              <NavLogoText>STAG.IO</NavLogoText>
            </NavLogo>
            <NavTabs>
              {TABS.map(t => (
                <NavTab key={t} $active={tab === t} onClick={() => setTab(t)}>
                  {t}
                  {t === "Notifications" && unread > 0 && (
                    <span style={{ marginLeft: "6px", background: "#ff3aaa", color: "#fff", borderRadius: "10px", padding: "1px 7px", fontSize: "10px", fontWeight: "700" }}>{unread}</span>
                  )}
                </NavTab>
              ))}
            </NavTabs>
            <NavRight>
              <ThemeToggleBtn onClick={() => setIsDark(p => !p)}>{isDark ? "☀ Light" : "🌙 Dark"}</ThemeToggleBtn>
              <GhostButton onClick={logout} style={{ padding: "6px 12px", border: "none", color: "#ff5064" }}>Logout</GhostButton>
              <NavAvatar title={fullName} onClick={() => setTab("Profile")}>
                {profile?.profile_image ? <img src={getImageUrl(profile.profile_image)} alt="Profile" /> : initials()}
              </NavAvatar>
            </NavRight>
          </Navbar>
          <Above>

          {/* ── HOME ── */}
          {tab === "Home" && (
            <>
              <Hero>
                <div>
                  <HeroLabel>Student Portal</HeroLabel>
                  <HeroTitle>Good morning, <span>{user?.first_name || "Student"}.</span></HeroTitle>
                  <HeroSub>Here's your internship search overview.</HeroSub>
                </div>
                <StatsRow>
                  <StatCard><StatValue $pink>{applications.length}</StatValue><StatLabel>Applied</StatLabel></StatCard>
                  <StatCard><StatValue>{applications.filter(a => a.status === "validated").length}</StatValue><StatLabel>Accepted</StatLabel></StatCard>
                  <StatCard><StatValue $pink>{mySkills.length}</StatValue><StatLabel>Skills</StatLabel></StatCard>
                </StatsRow>
              </Hero>
              <Content>
                {applyMsg && <SuccessMsg style={{ marginBottom: "16px" }}>{applyMsg}</SuccessMsg>}
                <ProfileCard style={{ marginBottom: "20px" }}>
                  <BigAvatar>
                    {profile?.profile_image ? <img src={getImageUrl(profile.profile_image)} alt="Profile" /> : initials()}
                  </BigAvatar>
                  <ProfileInfo>
                    <h3>{fullName}</h3>
                    <p style={{ marginBottom: "6px" }}>{user?.email}</p>
                    {lastActiveStr && <LastActiveBadge style={{ display: 'block', marginBottom: '10px' }}>{lastActiveStr}</LastActiveBadge>}
                    <TagsRow>
                      {mySkills.length > 0
                        ? mySkills.map((s, i) => <Tag key={i}>{s.name || s}</Tag>)
                        : <span style={{ fontSize: "12px", color: theme.textFaint, fontStyle: "italic" }}>No skills yet — go to Skills tab</span>
                      }
                    </TagsRow>
                  </ProfileInfo>
                  <GhostButton onClick={() => setTab("Profile")}>Edit Profile →</GhostButton>
                </ProfileCard>
                <SectionRow>
                  <SectionTitle>Latest Offers</SectionTitle>
                  <SeeAllBtn onClick={() => setTab("Internships")}>See all →</SeeAllBtn>
                </SectionRow>
                <CardGrid>
                  {offers.slice(0, 3).map(o => <OfferCard key={o.id} o={o} />)}
                </CardGrid>
              </Content>
            </>
          )}

          {/* ── INTERNSHIPS SEARCH ── */}
          {tab === "Internships" && (
            <>
              <Hero>
                <div>
                  <HeroLabel>Browse</HeroLabel>
                  <HeroTitle>Find <span>Internships</span></HeroTitle>
                  <HeroSub>{offers.length} offers available.</HeroSub>
                </div>
              </Hero>
              <Content>
                {applyMsg && <SuccessMsg style={{ marginBottom: "16px" }}>{applyMsg}</SuccessMsg>}
                <SearchBar>
                  <SearchInput
                    placeholder="Search by title or company..."
                    value={search}
                    onChange={e => setSearch(e.target.value)}
                  />
                  <FilterSelect value={filterWilaya} onChange={e => setFilterWilaya(e.target.value)}>
                    <option value="">All Wilayas</option>
                    <option value="Alger">Alger</option>
                    <option value="Oran">Oran</option>
                    <option value="Constantine">Constantine</option>
                    <option value="Annaba">Annaba</option>
                    <option value="Blida">Blida</option>
                    <option value="Setif">Setif</option>
                  </FilterSelect>
                </SearchBar>
                {offers.length === 0
                  ? <EmptyState><p>🔍</p><p>No offers found.</p></EmptyState>
                  : <CardGrid>{offers.map(o => <OfferCard key={o.id} o={o} />)}</CardGrid>
                }
              </Content>
            </>
          )}

          {/* ── APPLICATIONS ── */}
          {tab === "Applications" && (
            <>
              <Hero>
                <div>
                  <HeroLabel>Tracking</HeroLabel>
                  <HeroTitle>My <span>Applications</span></HeroTitle>
                  <HeroSub>Track your internship application statuses.</HeroSub>
                </div>
              </Hero>
              <Content>
                {applications.length === 0
                  ? <EmptyState><p>📭</p><p>No applications yet.</p></EmptyState>
                  : <GlassCard>
                    {applications.map(a => (
                      <AppRow key={a.id}>
                        <AppInfo>
                          <p>{a.offer_title || a.title || "Internship Application"}</p>
                          <span>{a.company_name || a.company} · Applied {a.created_at ? new Date(a.created_at).toLocaleDateString() : ""}</span>
                        </AppInfo>
                        <StatusBadge $s={a.status}>{a.status}</StatusBadge>
                        <PrivacyBtn
                          $on={a.visibility === 'public'}
                          onClick={() => handlePrivacyToggle(a.id, a.visibility || 'private')}
                          title={a.visibility === 'public' ? 'Public — click to make private' : 'Private — click to make public'}
                        >
                          {a.visibility === 'public' ? '🌍 Public' : '🔒 Private'}
                        </PrivacyBtn>
                        {a.status === "validated" && (
                          <GhostButton onClick={() => handleDownload(a.id)}>📄 Agreement</GhostButton>
                        )}
                      </AppRow>
                    ))}
                  </GlassCard>
                }
              </Content>
            </>
          )}

          {/* ── SKILLS ── */}
          {tab === "Skills" && (
            <>
              <Hero>
                <div>
                  <HeroLabel>My Skills</HeroLabel>
                  <HeroTitle>Manage <span>Skills</span></HeroTitle>
                  <HeroSub>Add skills to your profile so companies can find you.</HeroSub>
                </div>
              </Hero>
              <Content>
                <SectionTitle style={{ marginBottom: "14px" }}>My Current Skills</SectionTitle>
                <GlassCard style={{ marginBottom: "20px" }}>
                  {mySkills.length === 0
                    ? <p style={{ color: theme.textFaint, fontSize: "13px", fontStyle: "italic" }}>No skills added yet.</p>
                    : <TagsRow>
                      {mySkills.map(s => (
                        <SkillPill key={s.id}>
                          {s.name || s}
                          <button onClick={() => handleRemoveSkill(s.id)} title="Remove">×</button>
                        </SkillPill>
                      ))}
                    </TagsRow>
                  }
                </GlassCard>
                <SectionTitle style={{ marginBottom: "14px" }}>Available Skills — Click to Add</SectionTitle>
                <GlassCard>
                  <TagsRow>
                    {allSkills
                      .filter(s => !mySkills.some(ms => ms.id === s.id || ms === s.name))
                      .map(s => (
                        <GhostButton key={s.id} onClick={() => handleAddSkill(s.id)} style={{ fontSize: "12px", padding: "5px 12px" }}>
                          + {s.name}
                        </GhostButton>
                      ))
                    }
                  </TagsRow>
                </GlassCard>
              </Content>
            </>
          )}

          {/* ── NOTIFICATIONS ── */}
          {tab === "Notifications" && (
            <>
              <Hero>
                <div>
                  <HeroLabel>Inbox</HeroLabel>
                  <HeroTitle><span>{unread}</span> Unread</HeroTitle>
                  <HeroSub>Your latest activity notifications.</HeroSub>
                </div>
              </Hero>
              <Content>
                {notifs.length === 0
                  ? <EmptyState><p>🔔</p><p>No notifications yet.</p></EmptyState>
                  : <GlassCard>
                    {notifs.map(n => (
                      <AppRow key={n.id}>
                        <AppInfo>
                          <p>{!n.is_read && <NotifDot />}{n.message || n.text}</p>
                          <span>{n.created_at ? new Date(n.created_at).toLocaleDateString() : ""}</span>
                        </AppInfo>
                        {!n.is_read && <GhostButton onClick={() => handleMarkRead(n.id)}>Mark read</GhostButton>}
                      </AppRow>
                    ))}
                  </GlassCard>
                }
              </Content>
            </>
          )}

          {/* ── PROFILE ── */}
          {tab === "Profile" && (
            <ProfileTab user={user} profile={profile} setProfile={setProfile} initials={initials} getImageUrl={getImageUrl} />
          )}
        </Above>
      </PageBg>
    </ThemeProvider>
  );
}

// ── Profile edit tab ──────────────────────────────────────────────────────────
const AvatarUploadWrapper = styled.div`
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  margin-bottom: 30px;
`;
const AvatarCircle = styled.div`
  width: 130px; height: 130px; border-radius: 50%;
  background: ${({ theme }) => theme.bgInput};
  border: 3px solid transparent;
  background-clip: padding-box;
  position: relative; cursor: pointer; overflow: hidden;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;

  &::before {
    content: ''; position: absolute; top: -3px; left: -3px; right: -3px; bottom: -3px;
    z-index: -1; border-radius: 50%;
    background: linear-gradient(45deg, ${({ theme }) => theme.accentPink}, ${({ theme }) => theme.accent});
  }

  &:hover { transform: scale(1.05); }
  
  img { width: 100%; height: 100%; object-fit: cover; }
  
  .overlay {
    position: absolute; inset: 0; background: rgba(0, 0, 0, 0.6);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    opacity: 0; transition: opacity 0.3s; color: #fff; font-size: 12px; font-weight: 600;
  }
  .overlay span { font-size: 24px; margin-bottom: 4px; }
  &:hover .overlay { opacity: 1; }
`;
const AvatarInitials = styled.span`font-size: 40px; font-weight: 700; color: ${({ theme }) => theme.textMuted};`;
const HiddenInput = styled.input`display: none;`;

function ProfileTab({ user, profile, setProfile, initials, getImageUrl }) {
  const [form, setForm] = useState({
    github_link: profile?.github_link || "",
    portfolio_link: profile?.portfolio_link || "",
    wilaya: profile?.wilaya || "",
    bio: profile?.bio || "",
    internship_privacy: profile?.internship_privacy || "private",
  });
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const fileRef = useRef(null);
  const [previewUrl, setPreviewUrl] = useState(getImageUrl(profile?.profile_image));

  const handleChange = (e) => { setForm(p => ({ ...p, [e.target.name]: e.target.value })); setSuccess(""); };

  const handleSave = async (e) => {
    e.preventDefault(); setSaving(true);
    try {
      const res = await api.patch("/api/user/me/student/", {
        github_link: form.github_link,
        portfolio_link: form.portfolio_link,
        wilaya: form.wilaya,
        bio: form.bio,
        internship_privacy: form.internship_privacy,
      });
      setProfile(p => ({ ...p, ...res.data })); setSuccess("Profile updated!");
    } catch { setError("Update failed. Please try again."); }
    finally { setSaving(false); }
  };

  const handleImageUpload = async (e) => {
    const file = e.target.files[0]; if (!file) return;

    // Show instant preview
    const tempUrl = URL.createObjectURL(file);
    setPreviewUrl(tempUrl);
    setSuccess("Uploading image...");

    const fd = new FormData(); fd.append("profile_image", file);
    try {
      const res = await api.patch("/api/user/me/upload-profile-image/", fd, { headers: { "Content-Type": "multipart/form-data" } });
      setProfile(p => ({ ...p, profile_image: res.data.profile_image }));
      setPreviewUrl(getImageUrl(res.data.profile_image) || tempUrl);
      setSuccess("Profile picture updated successfully!");
    } catch {
      setError("Image upload failed.");
      setPreviewUrl(getImageUrl(profile?.profile_image) || ""); // Revert on fail
    }
  };

  return (
    <>
      <Hero>
        <div>
          <HeroLabel>Account</HeroLabel>
          <HeroTitle>My <span>Profile</span></HeroTitle>
          <HeroSub>
            {profile?.last_seen
              ? `Last active ${new Date(profile.last_seen).toLocaleString()}`
              : "This info is shown to companies when you apply."
            }
          </HeroSub>
        </div>
      </Hero>
      <Content>
        <FormCard>
          {success && <SuccessMsg>{success}</SuccessMsg>}
          {error && <ErrorMsg>{error}</ErrorMsg>}

          <AvatarUploadWrapper>
            <HiddenInput type="file" accept="image/*" ref={fileRef} onChange={handleImageUpload} />
            <AvatarCircle onClick={() => fileRef.current?.click()}>
              {previewUrl ? <img src={previewUrl} alt="Avatar" /> : <AvatarInitials>{initials()}</AvatarInitials>}
              <div className="overlay">
                <span>📷</span>
                Change Photo
              </div>
            </AvatarCircle>
          </AvatarUploadWrapper>

          <form onSubmit={handleSave}>
            {/* Bio — big standalone textarea */}
            <FormGroup>
              <Label>About Me / Portfolio Bio</Label>
              <BioTextarea
                name="bio"
                placeholder="Tell companies about yourself, your projects, what you're looking for..."
                value={form.bio}
                onChange={handleChange}
              />
            </FormGroup>

            {/* Links — each on its own line */}
            <FormGroup>
              <Label>👨‍💻 GitHub Profile</Label>
              <Input name="github_link" placeholder="https://github.com/yourusername" value={form.github_link} onChange={handleChange} />
            </FormGroup>
            <FormGroup>
              <Label>🌐 Portfolio / Personal Website</Label>
              <Input name="portfolio_link" placeholder="https://yourportfolio.com" value={form.portfolio_link} onChange={handleChange} />
            </FormGroup>

            <FormRow>
              <FormGroup>
                <Label>Wilaya</Label>
                <Input name="wilaya" placeholder="Alger, Oran..." value={form.wilaya} onChange={handleChange} />
              </FormGroup>
              <FormGroup>
                <Label>Internship Visibility</Label>
                <FilterSelect name="internship_privacy" value={form.internship_privacy} onChange={handleChange}>
                  <option value="private">🔒 Private — only me</option>
                  <option value="public">🌍 Public — everyone can see</option>
                  <option value="selected">✨ Selected — I choose which ones</option>
                </FilterSelect>
              </FormGroup>
            </FormRow>

            <SaveBtn type="submit" disabled={saving}>{saving ? "Saving..." : "Save Changes"}</SaveBtn>
          </form>
        </FormCard>
      </Content>
    </>
  );
}
