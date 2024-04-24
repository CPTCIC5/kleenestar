import axios from "axios";
import React from "react";
import Cookies from "js-cookie";
import useChatStore from "../store/store";

interface DeleteChatProps {
    isOpen: boolean;
    onClose: () => void;
    id: number;
}

const DeleteChat: React.FC<DeleteChatProps> = ({ isOpen, onClose, id }) => {
    const deleteConvo = useChatStore((state) => state.deleteConvo);

    const handleDeleteChat = async (id: number) => {
        try {
            await axios.delete(`http://127.0.0.1:8000/api/channels/convos/${id}/`, {
                withCredentials: true,
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": Cookies.get("csrftoken"),
                },
            });
            deleteConvo(id);
        } catch (err) {
            console.error("Error deleting chat", err);
        }
    };

    const onDeletion = () => {
        handleDeleteChat(id);
        onClose();
    };

    return (
        <>
            {isOpen ? (
                <div
                    className="fixed inset-0 z-50 bg-black bg-opacity-50 flex justify-center items-center p-3 mq436:p-0 mq436:items-end"
                    onClick={onClose}
                >
                    <div
                        className="max-w-[528.06px] w-full bg-white rounded-3xl mq436:rounded-t-3xl mq436:rounded-b-none"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="mx-[27.11px] py-[26.05px]">
                            <span className="max-w-[118px] w-full font-montserrat font-[600] text-[18px] leading-[21.94px] text-primary-300">
                                Delete chat?
                            </span>
                        </div>
                        <div className="border border-opacity-50 border-solid border-dimwhite w-full"></div>
                        <div className="pt-[22.94px] pb-[31.41px] mx-[26.94px] flex flex-col justify-start gap-[23.94px]">
                            <span className="max-w-[295px] w-full font-montserrat font-[400] text-[16px] leading-[19.5px] text-primary-300">
                                This will delete{" "}
                                <span className="font-[600]">Campaign overview.</span>
                            </span>
                            <div className="flex justify-start items-center gap-[23.64px]">
                                <button
                                    onClick={onClose}
                                    className="w-[107px] h-[40px] outline-none bg-primary-300 text-white rounded-full flex items-center justify-center font-montserrat font-[400] text-[15px] leading-[18.29px] hover:bg-primary-200 active:bg-primary-300 "
                                >
                                    Cancel
                                </button>
                                <button
                                    onClick={onDeletion}
                                    className="w-[105px] h-[40px] outline-none bg-white text-orangered-300 border border-solid border-orangered-300 rounded-full flex items-center justify-center font-montserrat font-[400] text-[15px] leading-[18.29px] hover:bg-orangered-100 hover:text-white hover:bg-opacity-60 "
                                >
                                    Delete
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            ) : null}
        </>
    );
};

export default DeleteChat;
