import { CircleX, PencilLine } from "lucide-react";
import React, { useState } from "react";
import PrimaryButton from "../components/PrimaryButton";

interface ChatFeedbackProps {
    isOpen: boolean;
    onClose: () => void;
}

const ChatFeedback: React.FC<ChatFeedbackProps> = ({ isOpen, onClose }) => {
    const options = [
        "Don’t like the style",
        "Refused when it shouldn’t have",
        "Didn’t fully follow instructions",
        "Not factually correct",
        "Being lazy",
        "Other",
    ];

    const [selectedOptions, setSelectedOptions] = useState<string[]>([]);
    const [note, setNote] = useState<string>("");

    const handleOptionChange = (option: string) => {
        setSelectedOptions((prevState) =>
            prevState.includes(option)
                ? prevState.filter((opt) => opt !== option)
                : [...prevState, option],
        );
    };
    const handleNoteChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setNote(event.target.value);
    };

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        // Send selectedOptions
        console.log(selectedOptions, note);

        // add axios API call
    };

    return (
        <>
            {isOpen ? (
                <div
                    className="fixed inset-0 z-50 bg-black bg-opacity-50 flex justify-center items-center p-3 mq436:p-0 mq436:items-end"
                    onClick={onClose}
                >
                    <div
                        className="max-w-[527.61px] w-full bg-white rounded-3xl mq436:rounded-t-3xl mq436:rounded-b-none"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <div className="ml-[27.11px] mr-[18.5px] pt-[19.05px] pb-[18.5px] flex items-center justify-between gap-2">
                            <div>
                                <span className="max-w-[262px] w-full font-montserrat font-[600] text-[18px] leading-[21.94px] text-primary-300">
                                    Provide additional feedback
                                </span>
                            </div>
                            <CircleX
                                onClick={onClose}
                                className="h-[38px] w-[38px] text-primary-300 bg-transparent"
                                strokeWidth={1}
                            />
                        </div>
                        <div className="border border-opacity-50 border-solid border-dimwhite w-full"></div>
                        <div className=" w-full  pl-[25.11px] pr-[30.03px] rounded-b-full">
                            <form
                                onSubmit={handleSubmit}
                                className="w-full pb-[26.05px] pt-[20.22px] flex flex-col  "
                            >
                                <div className="max-w-[470.47px] w-full flex flex-wrap gap-[8.47px] mb-[19.81px]">
                                    {options.map((option) => (
                                        <button
                                            key={option}
                                            className={`pl-[19px] pr-[22px] pt-[12.79px] pb-[14.21px] rounded-full w-fit h-fit border border-solid border-primary-300 font-montserrat font-[400] text-[15px] leading-[18.29px] ${
                                                selectedOptions.includes(option)
                                                    ? "bg-primary-300 text-white"
                                                    : "bg-white text-primary-300 border-opacity-15 "
                                            }`}
                                            onClick={(e) => {
                                                e.preventDefault();
                                                handleOptionChange(option);
                                            }}
                                        >
                                            {option}
                                        </button>
                                    ))}
                                </div>

                                <div className="max-w-[470.47px] w-full flex flex-col gap-[10.33px] mb-[23.93px]">
                                    <span className="font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary-300">
                                        Note
                                    </span>

                                    <div className="relative w-full min-h-[51px] flex items-center ">
                                        <textarea
                                            name="note"
                                            placeholder="(Optional) Feel free to add specific details"
                                            onChange={handleNoteChange}
                                            className="bg-background rounded-t-3xl rounded-b-3xl w-full h-full px-4  pr-10 py-4 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300 outline-none focus:outline-primary-100 focus:outline resize-y"
                                            value={note}
                                        />
                                        {/* PrimaryInputBox component for note*/}
                                        <div className="absolute bg-background text-primary flex items-center right-4 bottom-4">
                                            <PencilLine className="bg-inherit" />
                                        </div>
                                    </div>
                                </div>

                                <div className="max-w-[470.47px] w-full h-[40px]">
                                    <PrimaryButton disabled={selectedOptions.length === 0}>
                                        Submit feedback
                                    </PrimaryButton>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            ) : null}
        </>
    );
};

export default ChatFeedback;
