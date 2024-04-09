import { ArchiveRestore, CircleX, Trash2 } from "lucide-react";
import React from "react";
import archiveChats from "../utils/dummyArchiveChats.json";

interface ArchiveChatsProps {
    // define your props here
    isOpen: boolean;
    onClose: (option: boolean) => void;
}

const ArchiveChats: React.FC<ArchiveChatsProps> = ({ isOpen, onClose }) => {
    const chats = archiveChats.chat;
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
                                    {chats.map((chat) => {
                                        return (
                                            <div className="w-full flex flex-col gap-[10.5px] bg-white rounded-3xl p-[17.75px] pl-[18.19px]">
                                                <span className="font-montserrat font-[600] text-[15px] leading-[18.29px] text-primary-300">
                                                    {chat.title}
                                                </span>
                                                <div className="flex items-start justify-between">
                                                    <span className="font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300 mr-[15px]">
                                                        {chat.date}
                                                    </span>

                                                    <div className="flex justify-between max-w-[70.68px] w-full">
                                                        <div className="rounded-full h-[26px] py-[3px] px-[1px] mr-[10px]  hover:bg-primary-300 hover:bg-opacity-25">
                                                            <ArchiveRestore className="h-[20px] bg-transparent text-primary-300   " />
                                                        </div>
                                                        <div className="rounded-full h-[26px] py-[3px] px-[1px] hover:bg-orangered-200 hover:bg-opacity-25">
                                                            <Trash2 className="h-[20px] bg-transparent text-orangered-200  " />
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
