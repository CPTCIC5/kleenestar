import { ArchiveRestore, CircleX, Trash2 } from "lucide-react";
import React, { useEffect } from "react";
import axios from "axios";
import Cookies from "js-cookie";
import useChatStore from "../store/store";

interface ArchiveChatsProps {
    isOpen: boolean;
    onClose: (option: boolean) => void;
    isOpenDelete: boolean;
    onCloseDelete: (option: boolean) => void;
    setDeleteId: (id: number) => void;
}

interface Chat {
    id: number;
    created_at: string;
    title: string;
}

const ArchiveChats: React.FC<ArchiveChatsProps> = ({
    isOpen,
    onClose,
    isOpenDelete,
    onCloseDelete,
    setDeleteId,
}) => {
    const convos = useChatStore((state) => state.convos);
    const unarchiveConvo = useChatStore((state) => state.unarchiveConvo);
    const [chats, setChats] = React.useState<Chat[]>([]);

    useEffect(() => {
        const archivedConvos = convos.filter((convo) => convo.archived);

        const formattedConvos = archivedConvos.map((convo) => {
            const date = new Date(convo.created_at);
            const options = { year: "numeric", month: "long", day: "numeric" } as const;
            const formattedDate = new Intl.DateTimeFormat("en-US", options).format(date);

            return {
                id: convo.id,
                created_at: formattedDate,
                title: convo.title,
            };
        });

        setChats(formattedConvos);
    }, [convos]);

    const handleUnarchiveChat = async (id: number) => {
        try {
            await axios.patch(
                `http://127.0.0.1:8000/api/channels/convos/${id}/`,
                {
                    archived: false,
                },
                {
                    withCredentials: true,
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": Cookies.get("csrftoken"),
                    },
                },
            );
            unarchiveConvo(id);
            console.log(convos);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <>
            {isOpen ? (
                <div
                    className="fixed inset-0 z-50 bg-black bg-opacity-30 flex items-center p-0 justify-end"
                    onClick={() => onClose(isOpen)}
                >
                    <div
                        className=" max-w-[551px] w-full h-full bg-whitesmoke rounded-l-3xl flex flex-col items-start rounded-tl-3xl overflow-auto mq551:rounded-l-none "
                        onClick={(e) => e.stopPropagation()}
                    >
                        <CircleX
                            onClick={() => onClose(isOpen)}
                            className="absolute z-10 top-[25px] right-[32px] h-[38px] w-[38px] text-primary-300 bg-transparent mq551:h-[28px] mq551:w-[28px] mq551:top-[10px] mq551:right-[10px]"
                            strokeWidth={1}
                        />
                        <div className="w-full pt-[42.5px] pl-[80px] pb-[19px] flex gap-[19px] mq551:fixed mq551:bg-white mq551:flex mq551:items-center mq551:justify-center mq551:pl-0 ">
                            <span className="font-syne font-[700] text-[30px] leading-[36px] text-primary-300 mq374:text-[25px] ">
                                Archived chats
                            </span>
                        </div>

                        <div className="w-full h-full pl-[80px] flex flex-col mq551:mt-[120px] mq551:pl-0 mq551:flex mq551:flex-col mq551:items-center ">
                            <div className="max-w-[387px] w-full font-montserrat font-[400] text-[16px] leading-[19.5px] text-primary-300 text-start mb-[18px] mq551:text-center mq551:px-4">
                                Manage your archived chats here.
                            </div>
                            <div className="w-full h-full flex flex-col justify-between mq551:px-4 mq551:items-center">
                                <div className="max-w-[388.62px] w-full flex flex-col gap-[18px]">
                                    {chats.map((convo) => {
                                        return (
                                            <div
                                                key={convo.id}
                                                className="w-full flex flex-col gap-[10.5px] bg-white rounded-3xl p-[17.75px] pl-[18.19px]"
                                            >
                                                <span className="font-montserrat font-[600] text-[15px] leading-[18.29px] text-primary-300">
                                                    {convo.title}
                                                </span>
                                                <div className="flex items-start justify-between">
                                                    <span className="font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300 mr-[15px]">
                                                        {convo.created_at}
                                                    </span>

                                                    <div className="flex justify-between max-w-[70.68px] w-full">
                                                        <div className="rounded-full h-[26px] py-[3px] px-[1px] mr-[10px]  hover:bg-primary-300 hover:bg-opacity-25">
                                                            <ArchiveRestore
                                                                onClick={() =>
                                                                    handleUnarchiveChat(convo.id)
                                                                }
                                                                className="h-[20px] bg-transparent text-primary-300   "
                                                            />
                                                        </div>
                                                        <div className="rounded-full h-[26px] py-[3px] px-[1px] hover:bg-orangered-200 hover:bg-opacity-25">
                                                            <Trash2
                                                                onClick={() => {
                                                                    setDeleteId(convo.id);
                                                                    onCloseDelete(isOpenDelete);
                                                                }}
                                                                className="h-[20px] bg-transparent text-orangered-200  "
                                                            />
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            ) : null}
        </>
    );
};

export default ArchiveChats;
