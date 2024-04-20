// import React, { useEffect, useState } from "react";
import { FunctionComponent, useRef, useState } from "react";
// import { CircleHelp, ImageUp, SendHorizonal, SquarePen } from "lucide-react";
// import NewChatDisplay from "../components/NewChatDisplay";
import ChatSideBar from "../components/ChatSideBar";
import ChatDisplay from "../components/ChatDisplay";
// import axios from "axios";
import InviteTeam from "../modals/InviteTeam";

const Chat: FunctionComponent = () => {
    const SideBar = useRef<HTMLDivElement>(null);
    const [inviteOpen, setInviteOpen] = useState(false);
    const handleHide = () => {
        if (SideBar.current) {
            if (SideBar.current.style.transform === "translateX(-100%)") {
                setTimeout(() => {
                    if (SideBar.current) {
                        SideBar.current.style.transform = "translateX(0)";
                    }
                }, 20); // Adjust this delay to match your transition duration

                SideBar.current.style.display = "block";
            } else {
                SideBar.current.style.transform = "translateX(-100%)";

                setTimeout(() => {
                    if (SideBar.current) {
                        SideBar.current.style.display = "none";
                    }
                }, 75); // Adjust this delay to match your transition duration
            }
        }
    };

    return (
        <div className="h-screen flex overflow-hidden">
            <ChatSideBar SideBar={SideBar} handleHide={handleHide} setInviteOpen={setInviteOpen} />
            <ChatDisplay handleHide={handleHide} />
            <InviteTeam isOpen={inviteOpen} onClose={setInviteOpen} />
        </div>
    );
};

export default Chat;
