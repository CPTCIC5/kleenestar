import { CircleX, Link, PencilLine } from "lucide-react";
import React from "react";
import PrimaryButton from "../components/PrimaryButton";
import PrimaryInputBox from "../components/PrimaryInputBox";

interface InviteTeamProps {
    // define your props here
    isOpen: boolean;
    onClose: (option: boolean) => void;
}

const InviteTeam: React.FC<InviteTeamProps> = ({ isOpen, onClose }) => {
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
                                Invite team
                            </span>
                        </div>

                        <div className="w-full h-full pl-[80px] flex flex-col mq551:mt-[120px] mq551:pl-0 mq551:flex mq551:flex-col mq551:items-center ">
                            <div className="max-w-[387px] w-full font-montserrat font-[400] text-[16px] leading-[19.5px] text-primary-300 text-start mb-[18px] mq551:text-center mq551:px-4">
                                Send email invites to members.
                            </div>
                            <div className="w-full h-full flex flex-col justify-between mq551:px-4 mq551:items-center">
                                <div className="max-w-[388.62px] w-full flex flex-col">
                                    <div className="relative w-full h-[45px] flex items-center mt-[18px] ">
                                        <PrimaryInputBox
                                            type="email"
                                            name="email"
                                            placeholder="@work-email.com"
                                            // onChange={handleEmailChange}
                                            className="focus:outline-primary-100 focus:outline bg-white"
                                            // value={email}
                                            required
                                        />
                                        {/* PrimaryInputBox component for email*/}
                                        <div className="absolute bg-inherit text-primary flex items-center right-4">
                                            <PencilLine className="bg-inherit " />
                                        </div>
                                    </div>
                                    <div className="h-[40px] max-w-[454px] w-full mt-[30px]">
                                        <PrimaryButton>Send Invite</PrimaryButton>
                                        {/* Use the PrimaryButton component */}
                                    </div>

                                    <div>
                                        <Link className="text-primary-300" />
                                        <span>Get a shareable invite link instead</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            ) : null}
        </>
    );
};

export default InviteTeam;
