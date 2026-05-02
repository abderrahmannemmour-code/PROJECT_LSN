// src/pages/admin/AdminDashboard.jsx
import { useState, useEffect } from "react";
import styled, { ThemeProvider } from "styled-components";
import { darkTheme, lightTheme, GlobalStyle, PageBg, BlobMid, Above, Navbar, NavLogo, NavLogoSquare, NavLogoImage, NavLogoText, NavTabs, NavTab, NavRight, ThemeToggleBtn, NavAvatar, Hero, HeroLabel, HeroTitle, HeroSub, StatsRow, StatCard, StatValue, StatLabel, Content, SectionRow, SectionTitle, GlassCard, Tag, TagsRow, GhostButton, DangerButton, SuccessButton, StatusBadge, EmptyState } from "../../theme";
import api from "../../api/axios";

const Row = styled.div`display:flex;align-items:center;gap:12px;padding:14px 0;border-bottom:1px solid ${({theme})=>theme.border};&:last-child{border-bottom:none;}flex-wrap:wrap;`;
const RowAvatar = styled.div`width:36px;height:36px;border-radius:50%;background:${({theme})=>theme.accentGrad};display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff;flex-shrink:0;`;
const RowInfo = styled.div`flex:1;p{font-size:13px;font-weight:500;color:${({theme})=>theme.text};}span{font-size:11px;color:${({theme})=>theme.textMuted};}`;
const BtnRow  = styled.div`display:flex;gap:8px;`;
const NotifDot = styled.span`width:7px;height:7px;border-radius:50%;background:${({theme})=>theme.accentPink};display:inline-block;margin-right:6px;`;

const MOCK_INTERNSHIPS = [
  { id:1, student:"Ahmed Benali",  company:"Djezzy",    title:"Frontend Intern", status:"pending",   date:"2025-04-10" },
  { id:2, student:"Sara Mansouri", company:"Sonatrach", title:"Python Intern",   status:"validated", date:"2025-04-08" },
  { id:3, student:"Karim Daoudi",  company:"Mobilis",   title:"Full-Stack Dev",  status:"rejected",  date:"2025-04-06" },
];
const MOCK_NOTIFS = [
  { id:1, text:"Djezzy accepted Ahmed Benali for Frontend Intern", read:false, time:"2h ago" },
  { id:2, text:"New company registered: TechSoft Algérie",          read:false, time:"5h ago" },
  { id:3, text:"Sara Mansouri internship validated",                read:true,  time:"1d ago" },
];

const TABS = ["Dashboard","Internships","Notifications","Statistics"];

export default function AdminDashboard() {
  const [isDark, setIsDark]             = useState(true);
  const [tab, setTab]                   = useState("Dashboard");
  const [internships, setInternships]   = useState(MOCK_INTERNSHIPS);
  const [notifs, setNotifs]             = useState(MOCK_NOTIFS);
  const [stats, setStats]               = useState(null);
  const theme = isDark ? darkTheme : lightTheme;

  useEffect(() => {
    api.get("/api/administration/statistics/").then(r=>setStats(r.data)).catch(()=>{});
  }, []);

  const validate = (id) => setInternships(p=>p.map(i=>i.id===id?{...i,status:"validated"}:i));
  const reject   = (id) => setInternships(p=>p.map(i=>i.id===id?{...i,status:"rejected"}:i));
  const markRead = (id) => setNotifs(p=>p.map(n=>n.id===id?{...n,read:true}:n));
  const unread   = notifs.filter(n=>!n.read).length;

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
                  {t}{t==="Notifications"&&unread>0&&<span style={{marginLeft:"6px",background:"#ff3aaa",color:"#fff",borderRadius:"10px",padding:"1px 7px",fontSize:"10px",fontWeight:"700"}}>{unread}</span>}
                </NavTab>
              ))}
            </NavTabs>
            <NavRight>
              <ThemeToggleBtn onClick={()=>setIsDark(p=>!p)}>{isDark?"☀ Light":"🌙 Dark"}</ThemeToggleBtn>
              <NavAvatar title="Admin">AD</NavAvatar>
            </NavRight>
          </Navbar>
          <Above>

          {tab==="Dashboard" && (
            <>
              <Hero>
                <div>
                  <HeroLabel>Administration</HeroLabel>
                  <HeroTitle>Admin <span>Dashboard</span></HeroTitle>
                  <HeroSub>Overview of all internship placements.</HeroSub>
                </div>
                <StatsRow>
                  <StatCard><StatValue>{internships.length}</StatValue><StatLabel>Total</StatLabel></StatCard>
                  <StatCard><StatValue $pink>{internships.filter(i=>i.status==="validated").length}</StatValue><StatLabel>Validated</StatLabel></StatCard>
                  <StatCard><StatValue>{internships.filter(i=>i.status==="pending").length}</StatValue><StatLabel>Pending</StatLabel></StatCard>
                  <StatCard><StatValue $pink>{unread}</StatValue><StatLabel>Notifs</StatLabel></StatCard>
                </StatsRow>
              </Hero>
              <Content>
                <SectionRow>
                  <SectionTitle>Recent Internships</SectionTitle>
                  <GhostButton onClick={()=>setTab("Internships")}>See all →</GhostButton>
                </SectionRow>
                <GlassCard>
                  {internships.map(i=>(
                    <Row key={i.id}>
                      <RowAvatar>{i.student.substring(0,2).toUpperCase()}</RowAvatar>
                      <RowInfo><p>{i.student}</p><span>{i.company} · {i.title}</span></RowInfo>
                      <StatusBadge $status={i.status==="validated"?"accepted":i.status==="rejected"?"rejected":"pending"}>
                        {i.status}
                      </StatusBadge>
                      {i.status==="pending" && (
                        <BtnRow>
                          <SuccessButton onClick={()=>validate(i.id)}>✓ Validate</SuccessButton>
                          <DangerButton  onClick={()=>reject(i.id)}>✕ Reject</DangerButton>
                        </BtnRow>
                      )}
                    </Row>
                  ))}
                </GlassCard>
              </Content>
            </>
          )}

          {tab==="Internships" && (
            <>
              <Hero>
                <div>
                  <HeroLabel>Manage</HeroLabel>
                  <HeroTitle>All <span>Internships</span></HeroTitle>
                  <HeroSub>Validate or reject internship agreements.</HeroSub>
                </div>
              </Hero>
              <Content>
                <GlassCard>
                  {internships.map(i=>(
                    <Row key={i.id}>
                      <RowAvatar>{i.student.substring(0,2).toUpperCase()}</RowAvatar>
                      <RowInfo><p>{i.student}</p><span>{i.company} · {i.title} · {i.date}</span></RowInfo>
                      <StatusBadge $status={i.status==="validated"?"accepted":i.status==="rejected"?"rejected":"pending"}>
                        {i.status}
                      </StatusBadge>
                      <BtnRow>
                        {i.status==="pending" && <>
                          <SuccessButton onClick={()=>validate(i.id)}>✓ Validate</SuccessButton>
                          <DangerButton  onClick={()=>reject(i.id)}>✕ Reject</DangerButton>
                        </>}
                        <GhostButton onClick={()=>alert("Agreement PDF download — coming when backend is ready!")}>📄 Agreement</GhostButton>
                      </BtnRow>
                    </Row>
                  ))}
                </GlassCard>
              </Content>
            </>
          )}

          {tab==="Notifications" && (
            <>
              <Hero>
                <div>
                  <HeroLabel>Inbox</HeroLabel>
                  <HeroTitle><span>{unread}</span> Unread Notifications</HeroTitle>
                  <HeroSub>Stay updated on internship activity.</HeroSub>
                </div>
              </Hero>
              <Content>
                <GlassCard>
                  {notifs.map(n=>(
                    <Row key={n.id}>
                      <RowInfo>
                        <p>{!n.read && <NotifDot />}{n.text}</p>
                        <span>{n.time}</span>
                      </RowInfo>
                      {!n.read && <GhostButton onClick={()=>markRead(n.id)}>Mark read</GhostButton>}
                    </Row>
                  ))}
                </GlassCard>
              </Content>
            </>
          )}

          {tab==="Statistics" && (
            <>
              <Hero>
                <div>
                  <HeroLabel>Analytics</HeroLabel>
                  <HeroTitle>Platform <span>Statistics</span></HeroTitle>
                  <HeroSub>Data from GET /api/administration/statistics/ — live when backend is ready.</HeroSub>
                </div>
              </Hero>
              <Content>
                <StatsRow style={{marginBottom:"24px",flexWrap:"wrap"}}>
                  <StatCard><StatValue>{stats?.total_students||"—"}</StatValue><StatLabel>Students</StatLabel></StatCard>
                  <StatCard><StatValue $pink>{stats?.total_companies||"—"}</StatValue><StatLabel>Companies</StatLabel></StatCard>
                  <StatCard><StatValue>{stats?.placed||"—"}</StatValue><StatLabel>Placed</StatLabel></StatCard>
                  <StatCard><StatValue $pink>{stats?.unplaced||"—"}</StatValue><StatLabel>Unplaced</StatLabel></StatCard>
                </StatsRow>
                <GlassCard>
                  <p style={{color:"rgba(200,160,255,0.4)",fontSize:"13px",textAlign:"center",padding:"20px"}}>
                    Full charts will be displayed here once your friend adds the statistics endpoints.
                  </p>
                </GlassCard>
              </Content>
            </>
          )}

        </Above>
      </PageBg>
    </ThemeProvider>
  );
}
