import { CircleX, PencilLine } from "lucide-react";
import React from "react";
import PrimaryButton from "../components/PrimaryButton";

interface HelpCenterProps {
    isOpen: boolean;
    onClose: () => void;
}

const HelpCenter: React.FC<HelpCenterProps> = ({ isOpen, onClose }) => {
    const options = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10],
    ];
    const [selectedOption, setSelectedOption] = React.useState<number>();

    const handleOptionChange = (option: number) => {
        setSelectedOption(option);
    };

    const categories = ["General", "Technical", "To improve", "Feedback", "Others"];

    const [selectedCategory, setSelectedCategory] = React.useState<string>();

    const handleCategoryChange = (category: string) => {
        setSelectedCategory(category);
    };
    const [message, setMessage] = React.useState<string>("");

    const handleMessageChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        setMessage(event.target.value);
    };

    const [selectedEmoji, setSelectedEmoji] = React.useState<string>();

    const handleEmojiChange = (emoji: string) => {
        setSelectedEmoji(emoji);
    };

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        // Send selectedOptions
        console.log(selectedOption, selectedCategory, message, selectedEmoji);

        // add axios API call
    };

    return (
        <>
            {isOpen ? (
                <div
                    className="fixed inset-0 z-50 bg-black bg-opacity-50 flex justify-center items-center p-3 mq612:p-0"
                    onClick={onClose}
                >
                    <div
                        className="relative max-w-[595.05px] w-full bg-white rounded-3xl mq612:rounded-none mq612:h-full mq612:max-w-full "
                        onClick={(e) => e.stopPropagation()}
                    >
                        <CircleX
                            onClick={onClose}
                            className="absolute z-10 h-[38px] w-[38px] text-primary-300 bg-transparent top-[18px] right-[18px] mq612:h-[25px] mq612:w-[25px] mq612:top-[31px] mq612:right-[29px] "
                            strokeWidth={1}
                        />
                        <div className="w-full pt-[24.99px] pb-[10.97] px-[27.11px] mq612:fixed mq612:bg-white mq612:pt-[29.5px] mq612:pb-[27.5px] mq612:px-[31.5px]">
                            <span className="font-montserrat font-[600] text-[18px] leading-[21.94px] text-primary-300">
                                Help center
                            </span>
                        </div>

                        <form
                            method="POST"
                            onSubmit={handleSubmit}
                            className="w-full h-full overflow-auto"
                        >
                            <div className="px-[27.11px] mb-[21.01px] mq612:mt-[81px] mq612:flex mq612:items-center mq612:justify-center mq612:bg-background mq612:pb-[19.5px] mq612:mb-0">
                                <span className="text-center font-montserrat font-[400] text-[14px] leading-[17.07px] text-primary-300 mq612:mt-[19.5px]">
                                    Let us know, we will improve as soon as possible.
                                </span>
                            </div>
                            <div className="border border-opacity-50 border-solid border-dimwhite w-full mb-[20.01px] mq612:hidden"></div>
                            <div className="pl-[25.11px] pr-[24.5px] pb-[25.01px] mq612:bg-background">
                                <div className="flex flex-col gap-[16px]">
                                    <div className="flex flex-col gap-[10.54px]">
                                        <span className="font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary-300">
                                            How urgent is it?
                                        </span>
                                        <div className="w-full flex  gap-[10.33px] mq612:flex-wrap mq612:flex-col mq612:items-center">
                                            {options.map((optionslist, index) => {
                                                return (
                                                    <div
                                                        key={index}
                                                        className="w-full flex gap-[10.33px] justify-between"
                                                    >
                                                        {optionslist.map((option) => {
                                                            return (
                                                                <button
                                                                    key={option}
                                                                    className={`h-[45px] w-[45px] rounded-full ${
                                                                        selectedOption === option
                                                                            ? "bg-primary-300 text-white"
                                                                            : "bg-whitesmoke text-primary-300"
                                                                    }`}
                                                                    onClick={(e) => {
                                                                        e.preventDefault();
                                                                        handleOptionChange(option);
                                                                    }}
                                                                >
                                                                    {option}
                                                                </button>
                                                            );
                                                        })}
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </div>

                                    <div className="w-full flex flex-col gap-[10.54px]">
                                        <span className="font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary-300">
                                            Category
                                        </span>
                                        <div className="w-full flex flex-wrap">
                                            {categories.map((category) => (
                                                <button
                                                    key={category}
                                                    className={`px-[20px] py-[12.79px] rounded-full font-montserrat font-[400] text-[15px] leading-[18.29px] ${
                                                        selectedCategory === category
                                                            ? "bg-primary-300 text-white"
                                                            : "bg-white text-primary-300 border-opacity-15 mq612:bg-background "
                                                    }`}
                                                    onClick={(e) => {
                                                        e.preventDefault();
                                                        handleCategoryChange(category);
                                                    }}
                                                >
                                                    {category}
                                                </button>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="w-full flex flex-col gap-[10.33px]">
                                        <span className="font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary-300">
                                            Message
                                        </span>

                                        <div className="relative w-full min-h-[51px] flex items-center ">
                                            <textarea
                                                name="message"
                                                placeholder="Tell us now and we will do it ASAP."
                                                onChange={handleMessageChange}
                                                className="bg-background rounded-t-3xl rounded-b-3xl w-full h-full px-4  pr-10 py-4 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300 outline-none focus:outline-primary-100 focus:outline mq612:outline-primary-100 mq612:outline-2 resize-y"
                                                value={message}
                                            />
                                            {/* PrimaryInputBox component for Message*/}
                                            <div className="absolute bg-background text-primary flex items-center right-4 bottom-4">
                                                <PencilLine className="bg-inherit" />
                                            </div>
                                        </div>
                                    </div>

                                    <div className="flex flex-col gap-[10.54px]">
                                        <span className="font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary-300">
                                            Give us emoji
                                        </span>
                                        <div className="flex gap-[17px] flex-wrap">
                                            <button
                                                className={`h-[45px] w-[45px] flex justify-center items-center rounded-full ${
                                                    selectedEmoji === "astonished"
                                                        ? "bg-primary-300 text-white"
                                                        : "bg-whitesmoke text-primary-300"
                                                }`}
                                                onClick={(e) => {
                                                    e.preventDefault();
                                                    handleEmojiChange("astonished");
                                                }}
                                            >
                                                <img
                                                    className="h-[30px] w-[30px]"
                                                    src="/public/astonished.svg"
                                                    alt=""
                                                />
                                            </button>
                                            <button
                                                className={`h-[45px] w-[45px] flex justify-center items-center rounded-full ${
                                                    selectedEmoji === "cry"
                                                        ? "bg-primary-300 text-white"
                                                        : "bg-whitesmoke text-primary-300"
                                                }`}
                                                onClick={(e) => {
                                                    e.preventDefault();
                                                    handleEmojiChange("cry");
                                                }}
                                            >
                                                <img
                                                    className="h-[30px] w-[30px]"
                                                    src="/public/cry.svg"
                                                    alt=""
                                                />
                                            </button>
                                            <button
                                                className={`h-[45px] w-[45px] flex justify-center items-center rounded-full ${
                                                    selectedEmoji === "unamused"
                                                        ? "bg-primary-300 text-white"
                                                        : "bg-whitesmoke text-primary-300"
                                                }`}
                                                onClick={(e) => {
                                                    e.preventDefault();
                                                    handleEmojiChange("unamused");
                                                }}
                                            >
                                                <img
                                                    className="h-[30px] w-[30px]"
                                                    src="/public/unamused.svg"
                                                    alt=""
                                                />
                                            </button>
                                            <button
                                                className={`h-[45px] w-[45px] flex justify-center items-center rounded-full ${
                                                    selectedEmoji === "smirking"
                                                        ? "bg-primary-300 text-white"
                                                        : "bg-whitesmoke text-primary-300"
                                                }`}
                                                onClick={(e) => {
                                                    e.preventDefault();
                                                    handleEmojiChange("smirking");
                                                }}
                                            >
                                                <img
                                                    className="h-[30px] w-[30px]"
                                                    src="/public/smirking.svg"
                                                    alt=""
                                                />
                                            </button>
                                            <button
                                                className={`h-[45px] w-[45px] flex justify-center items-center rounded-full ${
                                                    selectedEmoji === "happy"
                                                        ? "bg-primary-300 text-white"
                                                        : "bg-whitesmoke text-primary-300"
                                                }`}
                                                onClick={(e) => {
                                                    e.preventDefault();
                                                    handleEmojiChange("happy");
                                                }}
                                            >
                                                <img
                                                    className="h-[30px] w-[30px]"
                                                    src="/public/happy.svg"
                                                    alt=""
                                                />
                                            </button>
                                            <button
                                                className={`h-[45px] w-[45px] flex justify-center items-center rounded-full ${
                                                    selectedEmoji === "more-happy"
                                                        ? "bg-primary-300 text-white"
                                                        : "bg-whitesmoke text-primary-300"
                                                }`}
                                                onClick={(e) => {
                                                    e.preventDefault();
                                                    handleEmojiChange("more-happy");
                                                }}
                                            >
                                                <img
                                                    className="h-[30px] w-[30px]"
                                                    src="/public/more-happy.svg"
                                                    alt=""
                                                />
                                            </button>
                                            <button
                                                className={`h-[45px] w-[45px] flex justify-center items-center rounded-full ${
                                                    selectedEmoji === "in-love"
                                                        ? "bg-primary-300 text-white"
                                                        : "bg-whitesmoke text-primary-300"
                                                }`}
                                                onClick={(e) => {
                                                    e.preventDefault();
                                                    handleEmojiChange("in-love");
                                                }}
                                            >
                                                <img
                                                    className="h-[30px] w-[30px]"
                                                    src="/public/in-love.svg"
                                                    alt=""
                                                />
                                            </button>
                                            <button
                                                className={`h-[45px] w-[45px] flex justify-center items-center rounded-full ${
                                                    selectedEmoji === "smiling"
                                                        ? "bg-primary-300 text-white"
                                                        : "bg-whitesmoke text-primary-300"
                                                }`}
                                                onClick={(e) => {
                                                    e.preventDefault();
                                                    handleEmojiChange("smiling");
                                                }}
                                            >
                                                <img
                                                    className="h-[30px] w-[30px]"
                                                    src="/public/smiling.svg"
                                                    alt=""
                                                />
                                            </button>
                                            <button
                                                className={`h-[45px] w-[45px] flex justify-center items-center rounded-full ${
                                                    selectedEmoji === "vomiting"
                                                        ? "bg-primary-300 text-white"
                                                        : "bg-whitesmoke text-primary-300"
                                                }`}
                                                onClick={(e) => {
                                                    e.preventDefault();
                                                    handleEmojiChange("vomiting");
                                                }}
                                            >
                                                <img
                                                    className="h-[30px] w-[30px]"
                                                    src="/public/vomiting.svg"
                                                    alt=""
                                                />
                                            </button>
                                        </div>
                                    </div>

                                    <div className="w-full h-[40px] mt-[28px]">
                                        <PrimaryButton
                                            disabled={
                                                !selectedCategory ||
                                                !selectedEmoji ||
                                                !selectedOption ||
                                                !message
                                            }
                                        >
                                            Submit feedback
                                        </PrimaryButton>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            ) : null}
        </>
    );
};

export default HelpCenter;
