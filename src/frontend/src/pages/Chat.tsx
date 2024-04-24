// import React, { useEffect, useState } from "react";
import { FunctionComponent, useEffect, useRef, useState } from "react";
// import { CircleHelp, ImageUp, SendHorizonal, SquarePen } from "lucide-react";
// import NewChatDisplay from "../components/NewChatDisplay";
import ChatSideBar from "../components/ChatSideBar";
import ChatDisplay from "../components/ChatDisplay";
// import axios from "axios";
import InviteTeam from "../modals/InviteTeam";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Cookies from "js-cookie";
import useChatStore from "../store/store";
import DeleteChat from "../modals/DeleteChat";
import ArchiveChats from "../modals/ArchiveChats";

const Chat: FunctionComponent = () => {
    const [isOpenDelete, setIsOpenDelete] = useState<boolean>(false);
    const [isOpenArchive, setIsOpenArchive] = useState<boolean>(false);
    const convos = useChatStore((state) => state.convos);
    const addConvos = useChatStore((state) => state.addConvos);
    const [currentConvoId, setCurrentConvoId] = useState<number>(convos[0]?.id);
    const [deleteId, setDeleteId] = useState<number>(-1);
    const navigate = useNavigate();
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userDetails, setUserDetails] = useState<{
        id: string;
        profile: { country: string };
    }>({
        id: "",
        profile: {
            country: "",
        },
    });

    const onCloseDelete = (option: boolean) => {
        setIsOpenDelete(!option);
    };

    if (isOpenDelete) {
        document.body.classList.add("overflow-y-hidden");
    } else {
        document.body.classList.remove("overflow-y-hidden");
    }

    const onCloseArchive = (option: boolean) => {
        setIsOpenArchive(!option);
    };

    if (isOpenArchive) {
        document.body.classList.add("overflow-y-hidden");
    } else {
        document.body.classList.remove("overflow-y-hidden");
    }

    useEffect(() => {
        const fetchWorkspaceDetails = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/workspaces/", {
                    withCredentials: true,
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": Cookies.get("csrftoken"),
                    },
                });
                setIsLoggedIn(true);
                setUserDetails(response.data[0].root_user);
            } catch (err) {
                console.error(err);
                navigate("/");
            }
        };
        fetchWorkspaceDetails();
    }, [navigate]);

    const fetchConvos = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/channels/convos/", {
                withCredentials: true,
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": Cookies.get("csrftoken"),
                },
            });
            addConvos(response.data.results);
            setCurrentConvoId(response.data.results[0].id);
        } catch (error) {
            console.error("Error fetching convos:", error);
        }
    };

    useEffect(() => {
        if (!isLoggedIn) return;
        fetchConvos();
    }, [isLoggedIn]);

    const SideBar = useRef<HTMLDivElement>(null);
    const [inviteOpen, setInviteOpen] = useState<boolean>(false);
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

    if (!isLoggedIn) {
        //redirect to login page if not logged in
        return <></>;
    }

    return (
        <div className="h-screen flex overflow-hidden">
            <ChatSideBar
                SideBar={SideBar}
                handleHide={handleHide}
                setInviteOpen={setInviteOpen}
                currentConvoId={currentConvoId}
                setCurrentConvoId={setCurrentConvoId}
                onCloseDelete={onCloseDelete}
                isOpenDelete={isOpenDelete}
                setDeleteId={setDeleteId}
            />
            <ChatDisplay
                handleHide={handleHide}
                currentConvoId={currentConvoId}
                onCloseArchive={onCloseArchive}
                isOpenArchive={isOpenArchive}
            />
            <InviteTeam isOpen={inviteOpen} onClose={setInviteOpen} />

            {isOpenArchive && (
                <ArchiveChats
                    isOpen={isOpenArchive}
                    onClose={() => onCloseArchive(isOpenArchive)}
                    onCloseDelete={onCloseDelete}
                    isOpenDelete={isOpenDelete}
                    setDeleteId={setDeleteId}
                />
            )}

            {isOpenDelete && (
                <DeleteChat
                    isOpen={isOpenDelete}
                    onClose={() => onCloseDelete(isOpenDelete)}
                    id={deleteId}
                />
            )}
        </div>
    );
};

export default Chat;
