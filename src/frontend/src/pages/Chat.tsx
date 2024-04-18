// import React, { useEffect, useState } from "react";
import { FunctionComponent } from "react";
import { CircleHelp, ImageUp, SendHorizonal } from "lucide-react";
import NewChatDisplay from "../components/NewChatDisplay";
import ChatSideBar from '../components/ChatSideBar';
// import axios from "axios";

const Chat: FunctionComponent = () => {
    // const [message, setMessage] = useState<{ role: string; content: string }>({
    //     role: "",
    //     content: "",
    // });
    // const [response, setResponse] = useState<string>("");
    // const [currentTitle, setCurrentTitle] = useState<string>("");
    // const [previousChat, setPreviousChat] = useState<object[]>([]); // Update the type argument to specify an array of objects
    // const apiKey = "YOUR_API_KEY"; // Replace 'YOUR_API_KEY' with your actual API key

    // const createNewChat = () => {
    //     setResponse("");
    //     setCurrentTitle("");
    // };

    // const sendMessage = async () => {
    //     try {
    //         const response = await axios.post(
    //             "https://api.openai.com/v1/completions",
    //             {
    //                 model: "text-davinci-002", // Adjust the model based on your preference
    //                 prompt: message,
    //                 max_tokens: 150,
    //             },
    //             {
    //                 headers: {
    //                     "Content-Type": "application/json",
    //                     Authorization: `Bearer ${apiKey}`,
    //                 },
    //             },
    //         );

    //         // Update state with the response from the API
    //         setResponse(response.data.choices[0].text.trim());
    //     } catch (error) {
    //         console.error("Error fetching data:", error);
    //     }
    // };

    // useEffect(() => {
    //     if (!currentTitle && response && message.content) {
    //         setCurrentTitle(response);
    //     }

    //     if (currentTitle && response && message.content) {
    //         setPreviousChat((prev) => [
    //             ...previousChat,
    //             { title: currentTitle, role: message.role, content: message.content },
    //         ]);
    //         setMessage({ role: "", content: "" });
    //     }
    // }, [currentTitle, message]);

    return (
        <div className="h-screen w-full bg-background px-[63.55px] py-[47.38px]">
            <div className="flex w-full h-full gap-[38.32px] bg-inherit justify-center">
                {/* Chat Header */}
                <ChatSideBar/>
                {/* Chat Body */}
                <section className="rounded-3xl max-w-[960.56px] w-full h-full p-4 md:px-[91.97px] md:py-[21.35px] flex flex-col relative gap-[29.94px] scrollbar bg-white">
                    <div className=" w-full h-full flex flex-col overflow-auto ">
                        <div className="flex-1 ">
                            <NewChatDisplay />
                        </div>
                    </div>
                    {/* Chat body bottom */}
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
                    {/* note button */}
                    <div className="absolute bottom-[12.45px] right-[12.54px] bg-inherit text-primary-300 mq850:hidden ">
                        <CircleHelp className="bg-transparent" />
                    </div>
                </section>
            </div>
        </div>
    );
};

export default Chat;
