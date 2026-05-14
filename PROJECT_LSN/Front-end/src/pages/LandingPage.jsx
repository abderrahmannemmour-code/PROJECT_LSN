import React from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { 
  Globe, 
  Mail, 
  Layers,
  ShieldCheck,
  Zap,
  ArrowRight,
  Target,
  Sparkles
} from "lucide-react";

export default function LandingPage() {
  const navigate = useNavigate();
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-white text-gray-900 font-sans selection:bg-indigo-100 overflow-x-hidden">
      
      {/* NAVBAR */}
      <nav className="fixed top-0 left-0 w-full z-50 bg-white/80 backdrop-blur-xl border-b border-gray-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 h-20 flex justify-between items-center">
          <div className="flex items-center gap-2 group cursor-pointer" onClick={() => navigate('/')}>
            <div className="w-8 h-8 bg-indigo-600 rounded-lg group-hover:rotate-12 transition-transform shadow-md"></div>
            <span className="text-2xl font-black tracking-tighter text-indigo-600">
              Stag.io
            </span>
          </div>

          <div className="flex items-center gap-6">
            {!user ? (
              <>
                <button 
                  onClick={() => navigate('/login')}
                  className="text-sm font-bold text-gray-500 hover:text-indigo-600 transition-colors"
                >
                  Login
                </button>
                <button 
                  onClick={() => navigate('/register')}
                  className="px-6 py-2.5 bg-gray-900 text-white text-sm font-black rounded-full hover:bg-indigo-600 hover:scale-105 transition-all shadow-lg"
                >
                  Get Started
                </button>
              </>
            ) : (
              <button 
                onClick={() => navigate(`/${user.role}`)}
                className="flex items-center gap-2 px-6 py-2.5 bg-indigo-600 text-white text-sm font-black rounded-full hover:bg-indigo-700 hover:scale-105 transition-all shadow-md"
              >
                Go Home <ArrowRight size={16} />
              </button>
            )}
          </div>
        </div>
      </nav>

      {/* HERO SECTION */}
      <main className="pt-40 pb-32">
        <section className="relative px-6">
          <div className="max-w-5xl mx-auto text-center mb-24">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-50 border border-indigo-100 text-[11px] font-black text-indigo-600 uppercase tracking-widest mb-8 animate-fade-in">
              <Sparkles size={14} className="text-indigo-500" />
              The #1 internship platform in Algeria
            </div>

            <h1 className="text-7xl lg:text-9xl font-black text-gray-900 leading-[0.85] tracking-tighter mb-10 animate-slide-up">
              Level up your <br />
              <span className="text-indigo-600">career path.</span>
            </h1>

            <p className="text-xl text-gray-500 max-w-2xl mx-auto mb-12 font-medium leading-relaxed animate-fade-in [animation-delay:200ms]">
              Connecting Algeria's brightest students with industry leaders. 
              Find verified internships, track your applications, and launch your future.
            </p>

            <div className="flex flex-col sm:flex-row justify-center gap-6 animate-fade-in [animation-delay:400ms]">
              <button 
                onClick={() => navigate('/register')}
                className="px-10 py-5 bg-indigo-600 text-white rounded-2xl font-black text-lg shadow-xl hover:bg-indigo-700 hover:-translate-y-1 transition-all group"
              >
                <span className="flex items-center gap-2">
                  Start Searching <ArrowRight className="group-hover:translate-x-1 transition-transform" />
                </span>
              </button>
              <button 
                onClick={() => navigate('/register')}
                className="px-10 py-5 bg-white border border-gray-200 text-gray-700 rounded-2xl font-black text-lg hover:bg-gray-50 hover:-translate-y-1 transition-all shadow-sm"
              >
                Post an Internship Offer
              </button>
            </div>
          </div>

          {/* APP MOCKUP PREVIEW */}
          <div className="max-w-6xl mx-auto relative group animate-slide-up [animation-delay:600ms]">
            <div className="relative bg-white rounded-[40px] p-4 shadow-2xl shadow-indigo-100 border border-gray-100 overflow-hidden">
              <div className="bg-gray-50 rounded-[32px] overflow-hidden aspect-[16/9] relative border border-gray-200">
                <img 
                  src="https://images.unsplash.com/photo-1551434678-e076c223a692?q=80&w=2070&auto=format&fit=crop" 
                  alt="Dashboard Preview" 
                  className="w-full h-full object-cover opacity-80"
                />
                
                {/* FLOATING UI ELEMENTS */}
                <div className="absolute top-10 left-10 p-6 bg-white/90 backdrop-blur-md border border-white rounded-3xl shadow-xl animate-fade-in">
                  <div className="flex items-center gap-4 mb-4">
                    <div className="w-12 h-12 bg-indigo-100 rounded-2xl flex items-center justify-center text-indigo-600">
                      <Target size={24} />
                    </div>
                    <div>
                      <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Matching Score</p>
                      <p className="text-xl font-black text-gray-900">98.4% Match</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* FEATURES */}
        <section className="max-w-7xl mx-auto px-6 mt-40 grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            { 
              title: "Verified Listings", 
              desc: "Every company and offer is manually verified by our team for your safety.",
              icon: ShieldCheck,
              color: "text-indigo-600",
              bg: "bg-indigo-50"
            },
            { 
              title: "Smart Matching", 
              desc: "Our algorithm matches you with offers that fit your skills and career goals.",
              icon: Zap,
              color: "text-indigo-600",
              bg: "bg-indigo-50"
            },
            { 
              title: "Digital CV", 
              desc: "Build a professional profile that gets you noticed by top recruiters.",
              icon: Layers,
              color: "text-indigo-600",
              bg: "bg-indigo-50"
            }
          ].map((feature, idx) => (
            <div key={idx} className="p-10 bg-white border border-gray-100 rounded-[40px] hover:shadow-xl hover:border-gray-200 hover:-translate-y-1 transition-all group shadow-sm">
              <div className={`w-14 h-14 ${feature.bg} ${feature.color} rounded-2xl flex items-center justify-center mb-8 group-hover:scale-110 transition-transform`}>
                <feature.icon size={28} />
              </div>
              <h3 className="text-2xl font-black text-gray-900 mb-4 tracking-tight">{feature.title}</h3>
              <p className="text-gray-500 font-medium leading-relaxed">{feature.desc}</p>
            </div>
          ))}
        </section>
      </main>

      {/* FOOTER */}
      <footer className="border-t border-gray-100 pt-32 pb-12 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-16 mb-24">
          <div className="md:col-span-1 space-y-8">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-indigo-600 rounded-lg shadow-md"></div>
              <span className="text-3xl font-black tracking-tighter text-indigo-600">Stag.io</span>
            </div>
            <p className="text-gray-500 font-medium leading-relaxed">
              Empowering Algerian talent through meaningful connections.
            </p>
          </div>
          <div>
            <h4 className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-8">Platform</h4>
            <ul className="space-y-4 text-sm font-bold text-gray-600">
              <li className="hover:text-indigo-600 cursor-pointer transition-colors">Search Internship Offers</li>
              <li className="hover:text-indigo-600 cursor-pointer transition-colors">For Universities</li>
              <li className="hover:text-indigo-600 cursor-pointer transition-colors">For Companies</li>
            </ul>
          </div>
          <div>
            <h4 className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-8">Company</h4>
            <ul className="space-y-4 text-sm font-bold text-gray-600">
              <li className="hover:text-indigo-600 cursor-pointer transition-colors">About Us</li>
              <li className="hover:text-indigo-600 cursor-pointer transition-colors">Contact</li>
              <li className="hover:text-indigo-600 cursor-pointer transition-colors">Privacy</li>
            </ul>
          </div>
          <div>
            <h4 className="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-8">Social</h4>
            <div className="flex gap-4">
              <div className="w-10 h-10 bg-white border border-gray-200 rounded-xl flex items-center justify-center text-gray-500 hover:text-indigo-600 hover:border-indigo-100 shadow-sm transition-all cursor-pointer">
                <Globe size={20} />
              </div>
              <div className="w-10 h-10 bg-white border border-gray-200 rounded-xl flex items-center justify-center text-gray-500 hover:text-indigo-600 hover:border-indigo-100 shadow-sm transition-all cursor-pointer">
                <Mail size={20} />
              </div>
            </div>
          </div>
        </div>
        <div className="max-w-7xl mx-auto px-6 text-center pt-8 border-t border-gray-200">
          <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">
            © 2024 Stag.io · Built with passion in Algeria
          </p>
        </div>
      </footer>
    </div>
  );
}

