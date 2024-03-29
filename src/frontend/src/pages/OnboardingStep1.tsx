import { FunctionComponent } from "react";
import RoundArrowRightSvgrepoCom1 from "../components/RoundArrowRightSvgrepoCom1";
import GoogleOauthButton from "../components/GoogleOauthButton";

const OnboardingStep1: FunctionComponent = () => {
    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4">
            <div className="max-w-[722px] max-h-[684px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4 relative ">
                <div className="absolute top-5 left-5">
                    <RoundArrowRightSvgrepoCom1 />
                </div>
                <div className="max-width flex items-center justify-center box-border max-w-full text-11xl font-syne">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className=" m-0 text-inherit font-bold font-inherit inline-block z-[1]">
                            Account
                        </span>
                        <div className="max-width self-stretch text-base text-center font-montserrat z-[1] flex flex-col item-center">
                            <span>We suggest using the email address you use at work.</span>
                        </div>
                    </div>
                </div>

                <div className="max-w-[454px] w-full h-[303.3px] mt-[50.05px] flex flex-col gap-[16px]">
                    <div className="w-full h-[99.3px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Email*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <input
                                type="email"
                                placeholder="@work-email.com"
                                name="email"
                                className="bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary  text-opacity-50 outline-none"
                                required
                            />
                            <img
                                className="absolute bg-background flex items-center right-4"
                                alt=""
                                src="/pen2svgrepocom1.svg"
                            />
                        </div>

                        <div className="w-full h-[16pxpx] flex items-center justify-start">
                            <span className=" h-[16px] font-montserrat font-[300] text-[13px] leading-[15.85px] text-orangered-300">
                                Unauthorized email
                            </span>
                        </div>
                    </div>
                    <div className="w-full h-[72.33px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Password*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <input
                                type="password"
                                name="password"
                                placeholder="password"
                                className="bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary  text-opacity-50 outline-none"
                                required
                            />
                            <img
                                className="absolute bg-background flex items-center right-4"
                                alt=""
                                src="/component-62--3.svg"
                            />
                        </div>
                    </div>
                    <div className="w-full h-[99.3px] gap-[10px] flex flex-col justify-between">
                        <span className="w-full h-[17px] font-montserrat font-[500] text-[14px] leading-[17.07px] text-primary">
                            Confirm Password*
                        </span>
                        <div className="relative w-full h-[45px] flex items-center ">
                            <input
                                type="password"
                                placeholder="Confirm Password"
                                name="confirm_password"
                                className="bg-background rounded-full w-full h-full px-4  pr-10 font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary  text-opacity-50 outline-none"
                                required
                            />
                            <img
                                className="absolute bg-background flex items-center right-4"
                                alt=""
                                src="/component-62--3.svg"
                            />
                        </div>

                        <div className="w-full h-[16pxpx] flex items-center justify-start">
                            <span className=" h-[16px] font-montserrat font-[300] text-[13px] leading-[15.85px] text-orangered-300">
                                Password doesn’t match
                            </span>
                        </div>
                    </div>
                </div>

                <div className="h-[19px] w-[330px] flex items-center justify-center gap-1 mt-[17.07px]">
                    <img src="/group-555.svg" alt="" />
                    <span className="h-[17px] font-montserrat font-[400] text-[14px] leading-[17.07px]">
                        Send me emails with tips, news, and offers.
                    </span>
                </div>
                <button className="cursor-pointer bg-primary-300 text-white rounded-full w-full h-[40px] shrink-0 border-none p-0 self-stretch position-relative max-w-[454px] mx-auto font-montserrat font-[600] text-[15px] leading-[18.29px] text-center mt-[39px]">
                    Continue
                </button>

                <div className="w-full h-[25.47px] flex justify-center mt-[25px] items-center">
                    <GoogleOauthButton />
                </div>
            </div>
        </div>
    );
};

export default OnboardingStep1;
