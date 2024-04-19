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
    const [inviteOpen, setInviteOpen] = useState(false)
    const handleHide = () => {
        if (SideBar.current) {
            if (SideBar.current.style.transform === "translateX(-100%)") {
                  setTimeout(() => {
                    if (SideBar.current) { SideBar.current.style.transform = "translateX(0)";
                    }
                }, 20); // Adjust this delay to match your transition duration
               
                SideBar.current.style.display = "block";
            } else {
                  SideBar.current.style.transform = "translateX(-100%)"
                
                setTimeout(() => {
                    if (SideBar.current) {
                      SideBar.current.style.display = "none"
                    }
                }, 75); // Adjust this delay to match your transition duration
            }
        }
    };

    return (
        <div className="h-screen flex">
            <ChatSideBar SideBar={SideBar} handleHide={handleHide} setInviteOpen={setInviteOpen} />
            <ChatDisplay handleHide={handleHide} />
            <InviteTeam  isOpen={inviteOpen} onClose={setInviteOpen} />
        </div>
    );
};

export default Chat;

{
    /* <div className="h-screen w-full bg-background px-[63.55px] py-[47.38px]">
            <div className="flex w-full h-full gap-[38.32px] bg-inherit justify-center">
                <aside className="bg-inherit  max-w-[375.93px] w-full h-full flex flex-col gap-[26.18px]">
                    <div className="bg-white h-[86.91px] w-full flex items-center justify-between rounded-3xl px-[26.54px] py-[16.06px]">
                        <div className="flex items-center justify-center gap-[18.13px]">
                            <img className="w-[52.07px] h-[54.78px]" src="/group-672.svg" alt="" />
                            <span className="w-[156.02px] font-syne font-[700] text-[25px] leading-[30px]">
                                Kleenestar
                            </span>
                        </div>
                        <SquarePen className="w-[20.94px] h-[20.94px] cursor-pointer" />
                    </div>
                    <div className="bg-white max-h-[580.12px] h-full w-full rounded-3xl"></div>
                    <div className=" bg-white h-[124.61px] w-full rounded-3xl"></div>
                </aside>
                <section className="rounded-3xl max-w-[960.56px] w-full h-full p-4 md:px-[91.97px] md:py-[21.35px] flex flex-col relative gap-[29.94px] scrollbar bg-white">
                    <div className=" w-full h-full flex flex-col overflow-auto ">
                        <div className="flex-1 ">
                            <NewChatDisplay />
                        </div>
                    </div>
                    <div className="w-full flex flex-col gap-[16.39px] items-center">
                        <div className="relative flex item-center max-w-[776.62px] w-full h-[54.45px]">
                            <input
                                type="text"
                                name="message"
                                placeholder="Ask anything"
                                className="rounded-full w-full h-full px-14 font-montserrat font-[400] text-[16px] leading-[19.5px] text-primary-200 outline-1 outline outline-primary-200 focus:outline-primary-200  focus:outline"
                            />
                            <div
                                // onClick={sendMessage}
                                className="absolute top-1/2 transform -translate-y-1/2 text-white flex items-center right-3 p-2 rounded-full bg-primary-300 cursor-pointer"
                            >
                                <SendHorizonal className="bg-transparent " />
                            </div>
                            <div className="absolute top-1/2 transform -translate-y-1/2 bg-inherit text-primary-300 flex items-center left-4 cursor-pointer">
                                <ImageUp className="bg-transparent" />
                            </div>
                        </div>
                        <span className="max-w-[464.93px] w-full h-[15.71px] font-montserrat font-[400] text-[12px] leading-[14.63px] text-primary-300 text-center">
                            KleeneStar can make mistakes. Consider checking important information.
                        </span>
                    </div>
                    <div className="absolute bottom-[12.45px] right-[12.54px] bg-inherit text-primary-300 mq850:hidden ">
                        <CircleHelp className="bg-transparent" />
                    </div>
                </section>
            </div>
        </div> */
}
