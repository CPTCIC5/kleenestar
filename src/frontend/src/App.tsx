import { useEffect } from "react";
import { Routes, Route, useNavigationType, useLocation } from "react-router-dom";
import "./App.css";
import Login from "./pages/Login";
import OnboardingStep1 from "./pages/OnboardingStep1";
import OnboardingStep2 from "./pages/OnboardingStep2";
import OnboardingStep3 from "./pages/OnboardingStep3";
import OnboardingDone from "./pages/OnboardingDone";
import JoinWorkspace from "./pages/JoinWorkspace";
import RecoveryEmail from "./pages/RecoveryEmail";
import PasswordRecovery from "./pages/PasswordRecovery";
import PasswordSaved from "./pages/PasswordSaved";
import Chat from "./pages/Chat";
import ConnectChannels from "./pages/ConnectChannels";
import PlanBilling from "./pages/PlanBilling";
import Settings from "./pages/Settings";

function App() {
    const action = useNavigationType();
    const location = useLocation();
    const pathname = location.pathname;

    // Scroll to top on navigation
    useEffect(() => {
        if (action !== "POP") {
            window.scrollTo(0, 0);
        }
    }, [action, pathname]);

    // Set title and meta description
    useEffect(() => {
        let title = "";
        let metaDescription = "";

        switch (pathname) {
            case "/":
                title = "";
                metaDescription = "";
                break;
            case "/onboard/step1":
                title = "";
                metaDescription = "";
                break;
            case "/onboard/step2":
                title = "";
                metaDescription = "";
                break;
            case "/onboard/step3":
                title = "";
                metaDescription = "";
                break;
            case "/onboard/step4":
                title = "";
                metaDescription = "";
                break;
            case "/onboard/done":
                title = "";
                metaDescription = "";
                break;
            case "/join-workspace":
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
            case "/chat":
                title = "";
                metaDescription = "";
                break;
            case "/channels":
                title = "";
                metaDescription = "";
                break;
            case "/billing":
                title = "";
                metaDescription = "";
                break;
            case "/settings":
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
            <Route path="/" element={<Login />} />
            <Route path="/onboard/step1" element={<OnboardingStep1 />} />
            <Route path="/onboard/step2" element={<OnboardingStep2 />} />
            <Route path="/onboard/step3" element={<OnboardingStep3 />} />
            <Route path="/onboard/step4" />
            <Route path="/onboard/done" element={<OnboardingDone />} />
            <Route path="/join-workspace" element={<JoinWorkspace />} />
            <Route path="/recovery-email" element={<RecoveryEmail />} />
            <Route path="/password-recovery" element={<PasswordRecovery />} />
            <Route path="/password-saved" element={<PasswordSaved />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/channels" element={<ConnectChannels />} />
            <Route path="/billing" element={<PlanBilling />} />
            <Route path="/settings" element={<Settings />} />
        </Routes>
    );
}

export default App;
