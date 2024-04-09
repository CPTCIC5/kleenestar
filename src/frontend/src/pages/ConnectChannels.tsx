import { CircleArrowLeft, SquareArrowOutUpRight } from "lucide-react";
import { useNavigate } from "react-router-dom";
import json from "../utils/dummyConnectChannels.json";
import ChannelCard from "../components/ChannelCard";
import { useRef } from "react";

function ConnectChannels() {
    const channel: {
        name: string;
        image: string;
        description: string;
        connected: boolean;
        available: boolean;
    }[] = json.data.channels;

    const infoBox = useRef<HTMLDivElement>(null);
    const navigate = useNavigate();
    const handleInfo = () => {
        if (infoBox.current) {
            if (infoBox.current.style.display === "block") {
                infoBox.current.style.display = "none";
            } else {
                infoBox.current.style.display = "block";
            }
        }
    };
    return (
        <div className="w-full h-full min-h-screen mq750:mt-[81px] bg-background ">
            <div
                ref={infoBox}
                style={{
                    boxShadow:
                        "-2px -2px 10px rgba(0, 0, 0, 0.2), 2px -2px 10px rgba(0, 0, 0, 0.2), -2px 2px 10px rgba(0, 0, 0, 0.2), 2px 2px 10px rgba(0, 0, 0, 0.2)",
                }}
                className="hidden h-[148px] right-[13%] mq750:right-[48px] top-[68px] w-[213px] bg-white absolute rounded-[2rem] shadow-xl z-30  "
            >
                <div className="w-fit ml-[28px] flex gap-4 my-[20px]">
                    <SquareArrowOutUpRight className="w-[20px]" />
                    <span className="font-montserrat text-[15px] font-medium">Help & FAQ</span>
                </div>
                <div className="w-fit ml-[28px] flex gap-4 my-[20px]">
                    <SquareArrowOutUpRight className="w-[20px]" />
                    <span className="font-montserrat text-[15px] font-medium">Release Notes</span>
                </div>
                <div className="w-fit ml-[28px] flex gap-4 my-[20px]">
                    <SquareArrowOutUpRight className="w-[20px]" />
                    <span className="font-montserrat text-[15px] font-medium">
                        Terms & Policies
                    </span>
                </div>
            </div>
            <div className="w-full mq750:bg-white mq750:pb-[15px] mq750:pt-[30px] z-20 mq750:fixed max-w-screen  mq750:top-[0px] mq750:justify-between mq750:px-[32px] text-primary-300 items-center relative top-[69px] gap-[30px] flex pl-[50px]">
                <CircleArrowLeft className="w-[30px] h-[30px]  " onClick={() => navigate(-2)} />
                <span className="font-syne mq750:absolute mq750:w-[80%]  mq750:text-center  font-[700] mq750:text-[20px] text-[30px] leading-[36px]">
                    My channels
                </span>
            </div>
            <div className="w-full mq750:relative mq750:bottom-[100.5px] max-w-[1478px] font-montserrat font-[400] text-[16px]">
                <div className="w-full mq750:text-center flex mq750:px-[31.5px] px-[110px] justify-between relative top-[123.74px]">
                    <span className="w-full">Connect the marketing channels you use.</span>
                    <div
                        onClick={handleInfo}
                        className="mq750:fixed cursor-pointer z-30 mq750:right-[40px] mq398:top-[30px] mq750:top-[30px]   py-[1px] w-fit h-fit rounded-full font-bold px-[8px] flex items-center border-solid border-2 border-primary-300 text-primary-300"
                    >
                        ?
                    </div>
                </div>
            </div>
            <div className="w-full mq750:relative bg-background mq750:top-[50.83px] pb-10 flex-wrap gap-[35.8px] flex font-montserrat relative top-[175.83px]  justify-center">
                {channel.map((props) => {
                    return <ChannelCard {...props} />;
                })}
            </div>
        </div>
    );
}

export default ConnectChannels;
