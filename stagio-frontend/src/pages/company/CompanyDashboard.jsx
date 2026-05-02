// src/pages/company/CompanyDashboard.jsx
import { useState, useEffect, useRef } from "react";
import styled, { ThemeProvider } from "styled-components";
import {
  darkTheme, lightTheme, GlobalStyle, PageBg, BlobMid, Above,
  Navbar, NavLogo, NavLogoSquare, NavLogoImage, NavLogoText, NavTabs, NavTab,
  NavRight, ThemeToggleBtn, NavAvatar,
  Hero, HeroLabel, HeroTitle, HeroSub,
  StatsRow, StatCard, StatValue, StatLabel,
  Content, SectionRow, SectionTitle, SeeAllBtn,
  GlassCard, CardGrid, Tag, TagsRow,
  PrimaryButton, GhostButton, DangerButton, SuccessButton,
  FormCard, FormGroup, FormRow, Label, Input,
  SuccessMsg, ErrorMsg, StatusBadge, EmptyState, fadeIn
} from "../../theme";
import { useAuth } from "../../context/AuthContext";
import api from "../../api/axios";
import { getMyOffers, createOffer, updateOffer, deleteOffer, getApplicants, acceptApplication, rejectApplication, getNotifications, markNotifRead } from "../../api/companyApi";

// ── Extra styled bits ─────────────────────────────────────────────────────────
const OfferTitle    = styled.h3`font-size:14px;font-weight:600;color:${({theme})=>theme.text};line-height:1.3;margin-bottom:6px;`;
const OfferMeta     = styled.p`font-size:11px;color:${({theme})=>theme.textMuted};margin-bottom:10px;`;
const BtnRow        = styled.div`display:flex;gap:8px;flex-wrap:wrap;`;
const AppRow        = styled.div`display:flex;align-items:center;gap:12px;padding:14px 0;border-bottom:1px solid ${({theme})=>theme.border};&:last-child{border-bottom:none;}flex-wrap:wrap;`;
const AppAvatar     = styled.div`width:36px;height:36px;border-radius:50%;background:${({theme})=>theme.accentGrad};display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff;flex-shrink:0;`;
const AppInfo       = styled.div`flex:1;p{font-size:13px;font-weight:500;color:${({theme})=>theme.text};}span{font-size:11px;color:${({theme})=>theme.textMuted};}`;
const NotifDot      = styled.span`width:7px;height:7px;border-radius:50%;background:${({theme})=>theme.accentPink};display:inline-block;margin-right:6px;`;
const OfferPink     = styled.p`font-size:10px;font-weight:700;color:${({theme})=>theme.accentPink};letter-spacing:0.1em;text-transform:uppercase;margin-bottom:5px;`;

const OfferBanner = styled.div`
  height: 120px; background: ${({ theme }) => theme.bgNav};
  border-bottom: 1px solid ${({ theme }) => theme.border};
  position: relative; overflow: hidden;
  img { width: 100%; height: 100%; object-fit: cover; }
  .fallback { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 40px; background: ${({ theme }) => theme.bgBtn}; }
`;

const OfferCompany = styled.div`
  display: flex; align-items: center; gap: 10px; margin: -20px 0 14px;
  font-size: 11px; font-weight: 600; color: ${({ theme }) => theme.textSub}; text-transform: uppercase; letter-spacing: 0.1em;
`;

const CompanyLogo = styled.img`
  width: 40px; height: 40px; border-radius: 8px; border: 2px solid ${({ theme }) => theme.bgCard}; background: #fff; object-fit: cover;
`;

// Circular upload styles
const AvatarUploadWrapper = styled.div`display: flex; justify-content: center; margin-bottom: 24px;`;
const AvatarCircle = styled.div`
  width: 110px; height: 110px; border-radius: 50%;
  background: ${({ theme }) => theme.bgInput};
  border: 2px dashed ${({ theme }) => theme.borderHover};
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; overflow: hidden; position: relative;
  transition: transform 0.2s;
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


// ── Social Media Modal Styles ──
const ModalOverlay = styled.div`
  position: fixed; inset: 0; background: rgba(0,0,0,0.8); backdrop-filter: blur(5px);
  z-index: 1000; display: flex; align-items: center; justify-content: center;
  padding: 20px; animation: ${fadeIn} 0.2s ease;
`;
const SocialProfileCard = styled(GlassCard)`
  width: 100%; max-width: 400px; padding: 40px 20px 30px; text-align: center;
  position: relative; overflow: hidden; background: ${({theme})=>theme.bg};
`;
const CloseBtn = styled.button`
  position: absolute; top: 16px; right: 16px; background: none; border: none;
  color: ${({theme})=>theme.textMuted}; font-size: 24px; cursor: pointer;
  &:hover { color: ${({theme})=>theme.accentPink}; }
`;
const TikTokAvatar = styled.div`
  width: 120px; height: 120px; border-radius: 50%; margin: 0 auto 16px;
  background: ${({theme})=>theme.accentGrad}; padding: 3px;
  img, .initials-fallback { width: 100%; height: 100%; border-radius: 50%; border: 3px solid ${({theme})=>theme.bg}; object-fit: cover; }
  .initials-fallback { display: flex; align-items: center; justify-content: center; font-size: 32px; font-weight: 800; background: ${({theme})=>theme.bgCard}; color: ${({theme})=>theme.text}; }
`;
const SocialName = styled.h2`font-size: 24px; font-weight: 700; color: ${({theme})=>theme.text}; line-height: 1.1; margin-bottom: 4px;`;
const SocialHandle = styled.p`font-size: 13px; color: ${({theme})=>theme.textMuted}; margin-bottom: 20px; font-weight: 500;`;
const SocialStats = styled.div`display: flex; justify-content: center; gap: 30px; margin-bottom: 24px;`;
const StatItem = styled.div`text-align: center; p:first-child { font-size: 18px; font-weight: 700; color: ${({theme})=>theme.text}; } p:last-child { font-size: 11px; color: ${({theme})=>theme.textMuted}; text-transform: uppercase; }`;
const SocialBio = styled.div`font-size: 14px; color: ${({theme})=>theme.textSub}; line-height: 1.5; margin-bottom: 24px; padding: 0 10px;`;
const LinkRow = styled.div`display: flex; justify-content: center; gap: 12px; margin-bottom: 24px;`;
const SocialLink = styled.a`
  display: flex; align-items: center; gap: 6px; padding: 8px 16px;
  background: ${({theme})=>theme.bgBtn}; border: 1px solid ${({theme})=>theme.borderBtn};
  border-radius: 20px; color: ${({theme})=>theme.text}; font-size: 12px; font-weight: 600; text-decoration: none;
  transition: all 0.2s;
  &:hover { background: ${({theme})=>theme.accentGrad}; color: #fff; border-color: transparent; }
`;


// ── Mock fallbacks ────────────────────────────────────────────────────────────
const MOCK_OFFERS = [
  { id:1, title:"Frontend Developer Intern", wilaya:"Alger", duration:"3 months", skills:[{name:"React"},{name:"CSS"}],    applicants_count:3 },
  { id:2, title:"Backend Python Intern",     wilaya:"Oran",  duration:"2 months", skills:[{name:"Python"},{name:"Django"}], applicants_count:1 },
];
const MOCK_APPLICANTS = [
  { id:1, student_name:"Ahmed Benali",  student_email:"a.benali@univ.dz",   skills:[{name:"React"},{name:"JS"}],     status:"pending" },
  { id:2, student_name:"Sara Mansouri", student_email:"s.mansouri@univ.dz", skills:[{name:"Python"},{name:"React"}], status:"pending" },
  { id:3, student_name:"Karim Daoudi",  student_email:"k.daoudi@univ.dz",   skills:[{name:"CSS"},{name:"HTML"}],     status:"accepted" },
];

const TABS = ["Dashboard","My Offers","Applicants","Notifications"];

export default function CompanyDashboard() {
  const { user, logout } = useAuth();
  const [isDark, setIsDark]           = useState(true);
  const [tab, setTab]                 = useState("Dashboard");
  const [profile, setProfile]         = useState(null);
  const [offers, setOffers]           = useState(MOCK_OFFERS);
  const [selectedOffer, setSelectedOffer] = useState(null);
  const [applicants, setApplicants]   = useState([]);
  const [notifs, setNotifs]           = useState([]);
  const [loading, setLoading]         = useState(false);
  const [viewStudent, setViewStudent] = useState(null); // TikTok social profile view
  const theme = isDark ? darkTheme : lightTheme;

  useEffect(() => {
    api.get("/api/user/me/company/").then(r=>setProfile(r.data)).catch(()=>{});
    getMyOffers().then(r=>setOffers(r.data)).catch(()=>setOffers(MOCK_OFFERS));
    getNotifications().then(r=>setNotifs(r.data)).catch(()=>setNotifs([]));
  }, []);

  // Load applicants when Applicants tab is opened
  useEffect(() => {
    if (tab==="Applicants") {
      if (selectedOffer) {
        getApplicants(selectedOffer.id).then(r=>setApplicants(r.data)).catch(()=>setApplicants(MOCK_APPLICANTS));
      } else {
        // load all applicants from all offers
        Promise.all(offers.map(o => getApplicants(o.id).then(r=>r.data).catch(()=>[])))
          .then(results => setApplicants(results.flat()))
          .catch(() => setApplicants(MOCK_APPLICANTS));
      }
    }
  }, [tab, selectedOffer]);

  const companyName = profile?.company_name || user?.email || "Company";
  const initials = () => companyName.substring(0,2).toUpperCase();
  const unread = notifs.filter(n=>!n.is_read).length;

  const getImageUrl = (path) => {
    if (!path) return '';
    return path.startsWith('http') ? path : `http://127.0.0.1:8000${path}`;
  };

  const handleAccept = async (appId) => {
    try {
      await acceptApplication(appId);
      setApplicants(p=>p.map(a=>a.id===appId?{...a,status:"accepted"}:a));
    } catch { console.error("Accept failed"); }
  };

  const handleReject = async (appId) => {
    try {
      await rejectApplication(appId);
      setApplicants(p=>p.map(a=>a.id===appId?{...a,status:"rejected"}:a));
    } catch { console.error("Reject failed"); }
  };

  const handleMarkRead = async (id) => {
    try {
      await markNotifRead(id);
      setNotifs(p=>p.map(n=>n.id===id?{...n,is_read:true}:n));
    } catch { console.error("Mark read failed"); }
  };

  const handleDeleteOffer = async (id) => {
    try {
      await deleteOffer(id);
      setOffers(p=>p.filter(o=>o.id!==id));
    } catch {
      setOffers(p=>p.filter(o=>o.id!==id)); // remove from UI anyway
    }
  };

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
              {TABS.map(t=>(
                <NavTab key={t} $active={tab===t} onClick={()=>setTab(t)}>
                  {t}
                  {t==="Notifications"&&unread>0&&(
                    <span style={{marginLeft:"6px",background:"#ff3aaa",color:"#fff",borderRadius:"10px",padding:"1px 7px",fontSize:"10px",fontWeight:"700"}}>{unread}</span>
                  )}
                </NavTab>
              ))}
            </NavTabs>
            <NavRight>
              <ThemeToggleBtn onClick={()=>setIsDark(p=>!p)}>{isDark?"☀ Light":"🌙 Dark"}</ThemeToggleBtn>
              <GhostButton onClick={logout} style={{padding:"6px 12px", border:"none", color:"#ff5064"}}>Logout</GhostButton>
              <NavAvatar title={companyName} onClick={()=>setTab("Profile")}>
                {profile?.logo ? <img src={getImageUrl(profile.logo)} alt="Logo" /> : initials()}
              </NavAvatar>
            </NavRight>
          </Navbar>
          <Above>

          {/* ── DASHBOARD ── */}
          {tab==="Dashboard" && (
            <>
              <Hero>
                <div>
                  <HeroLabel>Company Portal</HeroLabel>
                  <HeroTitle>Welcome, <span>{companyName}.</span></HeroTitle>
                  <HeroSub>Manage your offers and find talented students.</HeroSub>
                </div>
                <StatsRow>
                  <StatCard><StatValue>{offers.length}</StatValue><StatLabel>Offers</StatLabel></StatCard>
                  <StatCard><StatValue $pink>{offers.reduce((s,o)=>s+(o.applicants_count||0),0)}</StatValue><StatLabel>Applicants</StatLabel></StatCard>
                  <StatCard><StatValue>{applicants.filter(a=>a.status==="accepted").length}</StatValue><StatLabel>Accepted</StatLabel></StatCard>
                  <StatCard><StatValue $pink>{unread}</StatValue><StatLabel>Notifs</StatLabel></StatCard>
                </StatsRow>
              </Hero>
              <Content>
                <SectionRow>
                  <SectionTitle>Your Offers</SectionTitle>
                  <PrimaryButton onClick={()=>setTab("My Offers")}>+ New Offer</PrimaryButton>
                </SectionRow>
                <CardGrid>
                  {offers.map(o=>(
                    <GlassCard key={o.id} style={{padding:0,overflow:'hidden'}}>
                      <OfferBanner>
                        {o.cover_image || profile?.logo
                          ? <img src={getImageUrl(o.cover_image || profile?.logo)} alt="offer" />
                          : <div className="fallback">💼</div>
                        }
                      </OfferBanner>
                      <div style={{padding:'0 20px 20px'}}>
                        <OfferCompany>
                          {profile?.logo && <CompanyLogo src={getImageUrl(profile.logo)} alt={companyName} />}
                          {companyName}
                        </OfferCompany>
                        <OfferTitle>{o.title}</OfferTitle>
                        <OfferMeta>📍 {o.wilaya||o.location} · {o.duration}</OfferMeta>
                        <TagsRow style={{marginBottom:"14px"}}>{(o.skills||[]).map((s,i)=><Tag key={i}>{s.name||s}</Tag>)}</TagsRow>
                        <GhostButton onClick={()=>{setSelectedOffer(o);setTab("Applicants");}}>
                          👥 {o.applicants_count||0} Applicants
                        </GhostButton>
                      </div>
                    </GlassCard>
                  ))}
                </CardGrid>
              </Content>
            </>
          )}

          {/* ── MY OFFERS ── */}
          {tab==="My Offers" && (
            <OffersTab offers={offers} setOffers={setOffers} setTab={setTab} setSelectedOffer={setSelectedOffer} handleDeleteOffer={handleDeleteOffer} profile={profile} getImageUrl={getImageUrl} />
          )}

          {/* ── APPLICANTS ── */}
          {tab==="Applicants" && (
            <>
              <Hero>
                <div>
                  <HeroLabel>Review</HeroLabel>
                  <HeroTitle>{selectedOffer?<><span>{selectedOffer.title}</span> — Applicants</>:<>All <span>Applicants</span></>}</HeroTitle>
                  <HeroSub>Accept or refuse student applications.</HeroSub>
                </div>
                {selectedOffer && <GhostButton onClick={()=>setSelectedOffer(null)}>← All Offers</GhostButton>}
              </Hero>
              <Content>
                {applicants.length===0
                  ? <EmptyState><p>📭</p><p>No applicants yet.</p></EmptyState>
                  : <GlassCard>
                      {applicants.map(a=>(
                        <AppRow key={a.id} style={{cursor:"pointer"}} onClick={(e) => {
                          if(e.target.tagName !== 'BUTTON') setViewStudent(a);
                        }}>
                          <AppAvatar>{(a.student_name||a.name||"?").substring(0,2).toUpperCase()}</AppAvatar>
                          <AppInfo>
                            <p>{a.student_name||a.name}</p>
                            <span>{a.student_email||a.email}</span>
                          </AppInfo>
                          <TagsRow style={{flex:1,margin:0}}>{(a.skills||[]).map((s,i)=><Tag key={i}>{s.name||s}</Tag>)}</TagsRow>
                          <StatusBadge $status={a.status==="accepted"?"accepted":a.status==="rejected"?"rejected":"pending"}>{a.status}</StatusBadge>
                          {a.status==="pending"&&(
                            <BtnRow>
                              <SuccessButton onClick={()=>handleAccept(a.id)}>✓ Accept</SuccessButton>
                              <DangerButton  onClick={()=>handleReject(a.id)}>✕ Refuse</DangerButton>
                            </BtnRow>
                          )}
                        </AppRow>
                      ))}
                    </GlassCard>
                }
              </Content>
            </>
          )}

          {/* ── NOTIFICATIONS ── */}
          {tab==="Notifications" && (
            <>
              <Hero>
                <div>
                  <HeroLabel>Inbox</HeroLabel>
                  <HeroTitle><span>{unread}</span> Unread Notifications</HeroTitle>
                  <HeroSub>Stay updated on student activity.</HeroSub>
                </div>
              </Hero>
              <Content>
                {notifs.length===0
                  ? <EmptyState><p>🔔</p><p>No notifications yet.</p></EmptyState>
                  : <GlassCard>
                      {notifs.map(n=>(
                        <AppRow key={n.id}>
                          <AppInfo>
                            <p>{!n.is_read&&<NotifDot/>}{n.message||n.text}</p>
                            <span>{n.created_at?new Date(n.created_at).toLocaleDateString():""}</span>
                          </AppInfo>
                          {!n.is_read&&<GhostButton onClick={()=>handleMarkRead(n.id)}>Mark read</GhostButton>}
                        </AppRow>
                      ))}
                    </GlassCard>
                }
              </Content>
            </>
          )}

          {/* ── PROFILE ── */}
          {tab==="Profile" && (
            <CompanyProfileTab profile={profile} setProfile={setProfile} getImageUrl={getImageUrl} />
          )}

          {/* ── STUDENT PROFILE MODAL (TikTok Style) ── */}
          {viewStudent && (
            <ModalOverlay onClick={(e) => { if(e.target===e.currentTarget) setViewStudent(null); }}>
              <SocialProfileCard>
                <CloseBtn onClick={()=>setViewStudent(null)}>×</CloseBtn>
                <TikTokAvatar>
                  {viewStudent.profile_image 
                    ? <img src={getImageUrl(viewStudent.profile_image)} alt="Avatar" /> 
                    : <div className="initials-fallback">{(viewStudent.student_name||viewStudent.name||"?").substring(0,2).toUpperCase()}</div>
                  }
                </TikTokAvatar>
                <SocialName>{viewStudent.student_name||viewStudent.name}</SocialName>
                <SocialHandle>@{((viewStudent.student_email||viewStudent.email)||"").split('@')[0]}</SocialHandle>
                
                <SocialStats>
                  <StatItem><p>{(viewStudent.skills||[]).length}</p><p>Skills</p></StatItem>
                  <StatItem><p>{viewStudent.status==="accepted"?"1":"0"}</p><p>Internships</p></StatItem>
                  <StatItem><p>📍</p><p>{viewStudent.wilaya||"DZ"}</p></StatItem>
                </SocialStats>

                <SocialBio>
                  {viewStudent.bio || "Hi! I am a student actively looking for an internship. I am passionate about learning and building great products. 🚀"}
                </SocialBio>

                <LinkRow>
                  {viewStudent.github_link && <SocialLink href={viewStudent.github_link} target="_blank">👨‍💻 GitHub</SocialLink>}
                  {viewStudent.portfolio_link && <SocialLink href={viewStudent.portfolio_link} target="_blank">🌐 Portfolio</SocialLink>}
                  {(!viewStudent.github_link && !viewStudent.portfolio_link) && <span style={{fontSize:"12px", color:theme.textMuted}}>No links added</span>}
                </LinkRow>

                <TagsRow style={{justifyContent:"center", marginBottom:"20px"}}>
                  {(viewStudent.skills||[]).map((s,i)=><Tag key={i}>{s.name||s}</Tag>)}
                </TagsRow>
                
                {viewStudent.status==="pending" && (
                  <BtnRow style={{justifyContent:"center"}}>
                    <PrimaryButton onClick={()=>{handleAccept(viewStudent.id); setViewStudent(p=>({...p,status:"accepted"}));}}>✓ Accept Student</PrimaryButton>
                  </BtnRow>
                )}
              </SocialProfileCard>
            </ModalOverlay>
          )}

        </Above>
      </PageBg>
    </ThemeProvider>
  );
}

// ── Offers management tab ─────────────────────────────────────────────────────
function OffersTab({ offers, setOffers, setTab, setSelectedOffer, handleDeleteOffer, profile, getImageUrl }) {
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing]   = useState(null);
  const [success, setSuccess]   = useState("");
  const [error, setError]       = useState("");
  const [form, setForm] = useState({ title:"", wilaya:"", duration:"", description:"", skills:"" });
  const [coverImgFile, setCoverImgFile] = useState(null);

  const handleChange = (e) => setForm(p=>({...p,[e.target.name]:e.target.value}));

  const handleImageChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setCoverImgFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    let tempCoverUrl = "";
    if (coverImgFile) {
      tempCoverUrl = URL.createObjectURL(coverImgFile);
    }

    const payload = { title:form.title, wilaya:form.wilaya, duration:form.duration, description:form.description, skills:form.skills.split(",").map(s=>s.trim()).filter(Boolean) };
    try {
      if (editing) {
        const r = await updateOffer(editing.id, payload);
        setOffers(p=>p.map(o=>o.id===editing.id?r.data:o));
        setSuccess("Offer updated!");
      } else {
        const r = await createOffer(payload);
        setOffers(p=>[...p, r.data]);
        setSuccess("Offer created!");
      }
      setForm({title:"",wilaya:"",duration:"",description:"",skills:""});
      setShowForm(false); setEditing(null);
      setTimeout(()=>setSuccess(""),3000);
    } catch {
      // fallback: add locally
      setOffers(p=>[...p,{id:Date.now(),...payload, cover_image: tempCoverUrl, skills:payload.skills.map(s=>({name:s})),applicants_count:0}]);
      setShowForm(false);
      setCoverImgFile(null);
      setSuccess("Offer saved (backend not ready yet)!");
      setTimeout(()=>setSuccess(""),3000);
    }
  };

  const startEdit = (offer) => {
    setEditing(offer);
    setForm({ title:offer.title, wilaya:offer.wilaya||"", duration:offer.duration||"", description:offer.description||"", skills:(offer.skills||[]).map(s=>s.name||s).join(", ") });
    setShowForm(true);
  };

  return (
    <>
      <Hero>
        <div>
          <HeroLabel>Manage</HeroLabel>
          <HeroTitle>My <span>Offers</span></HeroTitle>
          <HeroSub>Create and manage your internship offers.</HeroSub>
        </div>
      </Hero>
      <Content>
        {success && <SuccessMsg>{success}</SuccessMsg>}
        {error   && <ErrorMsg>{error}</ErrorMsg>}
        <SectionRow>
          <SectionTitle>{offers.length} active offers</SectionTitle>
          <PrimaryButton onClick={()=>{setShowForm(p=>!p);setEditing(null);setForm({title:"",wilaya:"",duration:"",description:"",skills:""});}}>
            {showForm?"✕ Cancel":"+ New Offer"}
          </PrimaryButton>
        </SectionRow>
        {showForm && (
          <FormCard style={{marginBottom:"24px"}}>
            <form onSubmit={handleSubmit}>
              <FormGroup><Label>Offer Title</Label><Input name="title" placeholder="Frontend Developer Intern" value={form.title} onChange={handleChange} required /></FormGroup>
              <FormGroup><Label>Cover Picture (Optional)</Label><Input type="file" accept="image/*" onChange={handleImageChange} style={{padding:"8px"}} /></FormGroup>
              <FormRow>
                <FormGroup><Label>Wilaya</Label><Input name="wilaya" placeholder="Alger..." value={form.wilaya} onChange={handleChange} required /></FormGroup>
                <FormGroup><Label>Duration</Label><Input name="duration" placeholder="3 months" value={form.duration} onChange={handleChange} required /></FormGroup>
              </FormRow>
              <FormGroup><Label>Required Skills (comma-separated)</Label><Input name="skills" placeholder="React, Python..." value={form.skills} onChange={handleChange} /></FormGroup>
              <FormGroup><Label>Description</Label><Input as="textarea" name="description" placeholder="Describe the internship..." value={form.description} onChange={handleChange} style={{minHeight:"70px",resize:"vertical",lineHeight:"1.5"}} /></FormGroup>
              <PrimaryButton type="submit">{editing?"Update Offer →":"Create Offer →"}</PrimaryButton>
            </form>
          </FormCard>
        )}
        {offers.length===0
          ? <EmptyState><p>📋</p><p>No offers yet.</p></EmptyState>
          : <CardGrid>
              {offers.map(o=>(
                <GlassCard key={o.id} style={{padding:0,overflow:'hidden'}}>
                  <OfferBanner>
                    {o.cover_image || profile?.logo
                      ? <img src={getImageUrl(o.cover_image || profile?.logo)} alt="offer" />
                      : <div className="fallback">💼</div>
                    }
                  </OfferBanner>
                  <div style={{padding:'0 20px 20px'}}>
                    <OfferCompany>
                      {profile?.logo && <CompanyLogo src={getImageUrl(profile.logo)} alt={profile?.company_name||"Company"} />}
                      {profile?.company_name||"Company"}
                    </OfferCompany>
                    <OfferTitle>{o.title}</OfferTitle>
                    <OfferMeta>📍 {o.wilaya||o.location} · {o.duration}</OfferMeta>
                    <TagsRow style={{marginBottom:"14px"}}>{(o.skills||[]).map((s,i)=><Tag key={i}>{s.name||s}</Tag>)}</TagsRow>
                    <div style={{display:"flex",gap:"8px",flexWrap:"wrap"}}>
                      <GhostButton onClick={()=>{setSelectedOffer(o);setTab("Applicants");}}>👥 {o.applicants_count||0}</GhostButton>
                      <GhostButton onClick={()=>startEdit(o)}>✏ Edit</GhostButton>
                      <DangerButton onClick={()=>handleDeleteOffer(o.id)}>Delete</DangerButton>
                    </div>
                  </div>
                </GlassCard>
              ))}
            </CardGrid>
        }
      </Content>
    </>
  );
}

// ── Company profile tab ───────────────────────────────────────────────────────
function CompanyProfileTab({ profile, setProfile, getImageUrl }) {
  const [form, setForm]       = useState({ company_name:profile?.company_name||"", phone:profile?.phone||"", address:profile?.address||"", description:profile?.description||"", website:profile?.website||"" });
  const [saving, setSaving]   = useState(false);
  const [success, setSuccess] = useState("");
  const [error, setError]     = useState("");
  const fileRef = useRef(null);
  const [previewUrl, setPreviewUrl] = useState(getImageUrl(profile?.logo));

  const handleChange = (e) => { setForm(p=>({...p,[e.target.name]:e.target.value})); setSuccess(""); setError(""); };

  const handleSave = async (e) => {
    e.preventDefault(); setSaving(true);
    try { const r = await api.patch("/api/user/me/company/", form); setProfile(r.data); setSuccess("Profile updated!"); }
    catch { setError("Update failed."); }
    finally { setSaving(false); }
  };

  const handleLogo = async (e) => {
    const file = e.target.files[0]; if(!file) return;
    
    const tempUrl = URL.createObjectURL(file);
    setPreviewUrl(tempUrl);
    setSuccess("Uploading logo...");

    const fd = new FormData(); fd.append("logo", file);
    try { 
      const r = await api.patch("/api/user/me/upload-logo/", fd, {headers:{"Content-Type":"multipart/form-data"}}); 
      setProfile(p => ({...p, logo: r.data.logo}));
      setPreviewUrl(getImageUrl(r.data.logo) || tempUrl);
      setSuccess("Logo updated successfully!"); 
    }
    catch { 
      setError("Logo upload failed."); 
      setPreviewUrl(getImageUrl(profile?.logo) || "");
    }
  };

  return (
    <>
      <Hero>
        <div>
          <HeroLabel>Account</HeroLabel>
          <HeroTitle>Company <span>Profile</span></HeroTitle>
          <HeroSub>Shown to students browsing your offers.</HeroSub>
        </div>
      </Hero>
      <Content>
        <FormCard>
          {success && <SuccessMsg>{success}</SuccessMsg>}
          {error   && <ErrorMsg>{error}</ErrorMsg>}
          <form onSubmit={handleSave}>
            <AvatarUploadWrapper>
              <HiddenInput type="file" accept="image/*" ref={fileRef} onChange={handleLogo} />
              <AvatarCircle onClick={() => fileRef.current?.click()}>
                {previewUrl ? <img src={previewUrl} alt="Logo" /> : <AvatarInitials>{form.company_name?.substring(0,2).toUpperCase()||"CO"}</AvatarInitials>}
                <div className="overlay">
                  <span>📷</span>
                  Change Logo
                </div>
              </AvatarCircle>
            </AvatarUploadWrapper>

            <FormGroup><Label>Company Name</Label><Input name="company_name" value={form.company_name} onChange={handleChange} /></FormGroup>
            <FormRow>
              <FormGroup><Label>Phone</Label><Input name="phone" placeholder="+213..." value={form.phone} onChange={handleChange} /></FormGroup>
              <FormGroup><Label>Wilaya</Label><Input name="address" placeholder="Alger..." value={form.address} onChange={handleChange} /></FormGroup>
            </FormRow>
            <FormGroup><Label>Website</Label><Input name="website" placeholder="https://..." value={form.website} onChange={handleChange} /></FormGroup>
            <FormGroup><Label>Description</Label><Input as="textarea" name="description" value={form.description} onChange={handleChange} style={{minHeight:"80px",resize:"vertical",lineHeight:"1.5"}} /></FormGroup>
            <PrimaryButton type="submit" disabled={saving}>{saving?"Saving...":"Save Changes"}</PrimaryButton>
          </form>
        </FormCard>
      </Content>
    </>
  );
}
