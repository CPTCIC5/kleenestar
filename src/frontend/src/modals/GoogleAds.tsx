import { Switch } from "@mui/material";
import { CircleX } from "lucide-react";
import React from "react";
import PrimaryButton from "../components/PrimaryButton";

interface GoogleAdsProps {
    // define your props here
    isOpen: boolean;
    onClose: (option: boolean) => void;
    connected: boolean;
    setConnected: (option: boolean) => void;
}

const GoogleAds: React.FC<GoogleAdsProps> = ({ isOpen, onClose, connected, setConnected }) => {
    // define your state and methods here

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setConnected(event.target.checked);
    };

    const handleDisconnect = () => {
        setConnected(false);
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
                                Google Ads
                            </span>
                            <div>
                                {connected ? (
                                    <Switch
                                        checked={connected}
                                        onChange={handleChange}
                                        inputProps={{ "aria-label": "controlled" }}
                                    />
                                ) : (
                                    <Switch
                                        checked={connected}
                                        onChange={handleChange}
                                        inputProps={{ "aria-label": "controlled" }}
                                    />
                                )}
                            </div>
                        </div>

                        <div className="w-full h-full pl-[80px] flex flex-col mq551:mt-[120px] mq551:pl-0 mq551:flex mq551:flex-col mq551:items-center ">
                            <div className="max-w-[387px] w-full font-montserrat font-[400] text-[16px] leading-[19.5px] text-primary-300 text-start mb-[18px] mq551:text-center mq551:px-4">
                                Integrate Google Ads with Kleenestar.
                            </div>
                            <div className="w-full h-full flex flex-col justify-between mq551:px-4 mq551:items-center">
                                <div className="rounded-3xl bg-white max-w-[388.56px] w-full">
                                    <div className="flex item-start w-full pt-[18px] pb-[17.97px] pl-[26.18px]">
                                        <span className="font-montserrat font-[600] text-[18px] leading-[21.94px] text-primary-300">
                                            Instructions
                                        </span>
                                    </div>
                                    <div className="border border-opacity-50 border-solid border-dimwhite w-full"></div>
                                    <div className="py-[19.53px] flex flex-col items-center gap-[11px] mq551:p-3">
                                        <div className="max-w-[337px] w-full">
                                            <div className="w-full flex flex-col items-start gap-[12px]">
                                                <span className="font-montserrat font-[600] text-[15px] leading-[18.29px] text-primary-300">
                                                    1. Start Connection
                                                </span>
                                                <span className="font-montserrat font-[400] text-[14px] leading-[17.07px] text-primary-300">
                                                    Click on the “Connect button.
                                                </span>
                                            </div>
                                        </div>
                                        <div className="max-w-[337px] w-full">
                                            <div className="w-full flex flex-col items-start gap-[12px]">
                                                <span className="font-montserrat font-[600] text-[15px] leading-[18.29px] text-primary-300">
                                                    2. Google Login
                                                </span>
                                                <span className="font-montserrat font-[400] text-[14px] leading-[17.07px] text-primary-300">
                                                    You’ll be redirected to a Google login page.
                                                    Enter your credentials for the Google account
                                                    associated with your Google Ads.
                                                </span>
                                            </div>
                                        </div>
                                        <div className="max-w-[337px] w-full">
                                            <div className="w-full flex flex-col items-start gap-[12px]">
                                                <span className="font-montserrat font-[600] text-[15px] leading-[18.29px] text-primary-300">
                                                    3. Grant Access
                                                </span>
                                                <span className="font-montserrat font-[400] text-[14px] leading-[17.07px] text-primary-300">
                                                    Review the permissions Kleenestar is requesting
                                                    (e.g., view and manage your Google Ads
                                                    campaigns) and click “Allow”.
                                                </span>
                                            </div>
                                        </div>
                                        <div className="max-w-[337px] w-full">
                                            <div className="w-full flex flex-col items-start gap-[12px]">
                                                <span className="font-montserrat font-[600] text-[15px] leading-[18.29px] text-primary-300">
                                                    4. Complete Setup
                                                </span>
                                                <span className="font-montserrat font-[400] text-[14px] leading-[17.07px] text-primary-300">
                                                    Once authorized, you’ll be redirected back to
                                                    Kleenestar with your Google Ads account
                                                    connected.
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div className="h-[40px] max-w-[388.56px] w-full mt-[10px] mb-[40px]">
                                    <PrimaryButton
                                        onClick={handleDisconnect}
                                        className="bg-inherit "
                                        disabled={!connected}
                                    >
                                        Disconnect
                                    </PrimaryButton>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            ) : null}
        </>
    );
};

export default GoogleAds;
