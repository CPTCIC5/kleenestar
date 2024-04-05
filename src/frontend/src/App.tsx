import { useEffect } from "react";
import { Routes, Route, useNavigationType, useLocation } from "react-router-dom";
import "./global.css";
import Login from "./pages/Login";
import GetStarted from "./pages/GetStarted";
import OnboardingStep1 from "./pages/OnboardingStep1";
import OnboardingStep2 from "./pages/OnboardingStep2";
import OnboardingDone from "./pages/OnboardingDone";
import JoinTeam from "./pages/JoinTeam";
import RecoveryEmail from "./pages/RecoveryEmail";
import PasswordRecovery from "./pages/PasswordRecovery";
import PasswordSaved from "./pages/PasswordSaved";
import Settings from "./pages/Settings";
import ConnectChannels from "./pages/ConnectChannels";
import PlanBilling from "./pages/PlanBilling";
import Chat from "./pages/Chat";
import ChatImageQuerySent from "./pages/ChatImageQuerySent";
import ChatImageQuery from "./pages/ChatImageQuery";
import ChatNew from "./pages/ChatNew";
import NewChatDisplay from "./components/NewChatDisplay";
import TempTester from "./modals/TempTester";

function App() {
    const action = useNavigationType();
    const location = useLocation();
    const pathname = location.pathname;

    useEffect(() => {
        if (action !== "POP") {
            window.scrollTo(0, 0);
        }
    }, [action, pathname]);

    useEffect(() => {
        let title = "";
        let metaDescription = "";

        switch (pathname) {
            case "/":
                title = "";
                metaDescription = "";
                break;
            case "/get-started":
                title = "";
                metaDescription = "";
                break;
            case "/onboardingstep1":
                title = "";
                metaDescription = "";
                break;
            case "/onboardingstep2":
                title = "";
                metaDescription = "";
                break;
            case "/onboardingdone":
                title = "";
                metaDescription = "";
                break;
            case "/join-team":
                title = "";
                metaDescription = "";
                break;
            case "/recovery-email":
                title = "";
                metaDescription = "";
                break;
            case "/password-recovery":


            
                title = "";
                metaDescription = "";
                break;
            case "/password-saved":
                title = "";
                metaDescription = "";
                break;
            case "/settings":
                title = "";
                metaDescription = "";
                break;
            case "/connect-channels":
                title = "";
                metaDescription = "";
                break;
            case "/plan-billing":
                title = "";
                metaDescription = "";
                break;
            case "/chat":
                title = "";
                metaDescription = "";
                break;
            case "/chatimage-querysent":
                title = "";
                metaDescription = "";
                break;
            case "/chatimage-query":
                title = "";
                metaDescription = "";
                break;
            case "/chatnew":
                title = "";
                metaDescription = "";
                break;
        }

        if (title) {
            document.title = title;
        }

        if (metaDescription) {
            const metaDescriptionTag: HTMLMetaElement | null = document.querySelector(
                'head > meta[name="description"]',
            );
            if (metaDescriptionTag) {
                metaDescriptionTag.content = metaDescription;
            }
        }
    }, [pathname]);

    return (
        <Routes>
            <Route path="/" element={<TempTester/>} />
            <Route path="/get-started" element={<GetStarted />} />
            <Route path="/onboardingstep1" element={<OnboardingStep1 />} />
            <Route path="/onboardingstep2" element={<OnboardingStep2 />} />
            <Route path="/onboardingdone" element={<OnboardingDone />} />
            <Route path="/join-team" element={<JoinTeam />} />
            <Route path="/recovery-email" element={<RecoveryEmail />} />
            <Route path="/password-recovery" element={<PasswordRecovery />} />
            <Route path="/password-saved" element={<PasswordSaved />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/connect-channels" element={<ConnectChannels />} />
            <Route path="/plan-billing" element={<PlanBilling />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/chatimage-querysent" element={<ChatImageQuerySent />} />
            <Route path="/chatimage-query" element={<ChatImageQuery />} />
            <Route path="/chatnew" element={<ChatNew />} />
        </Routes>
    );
}
export default App;
