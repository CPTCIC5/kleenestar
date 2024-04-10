import { FunctionComponent } from "react";
import PrimaryButton from "../components/PrimaryButton";

const OnboardingDone: FunctionComponent = () => {
    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4 flex-col gap-[30px]">
            <div className="hidden mq551:block">
                <img src={"/public/MainLogo.svg"} alt="" />
            </div>
            <div className="max-w-[722px] max-h-[684px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4 bg-white">
                <div className="max-width flex items-center justify-center box-border max-w-full">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className="font-syne m-0  font-[700] text-[30px] font-inherit inline-block z-[1] leading-[36px] text-primary-300">
                            Welcome
                        </span>
                        <div className="max-width self-stretch text-[16px] leading-[19.5px] text-center font-montserrat z-[1] font-[400] text-primary-300 flex flex-col">
                            <span>Congratulations you are all set</span>
                            <span>Go to your workspace, connect your advertising </span>
                            <span>channels, and start learning.</span>
                        </div>
                    </div>
                </div>

                <div className="max-w-[454px] w-full mt-[54px]">
                    <img
                        src="/welcome-onboard-done-img.svg"
                        alt=""
                        className="max-w-full h-auto block m-auto "
                    />
                </div>

                <div className="h-[40px] max-w-[454px] w-full mt-[68px]">
                    <PrimaryButton>Get started</PrimaryButton>
                    {/* Use the PrimaryButton component */}
                </div>
            </div>
        </div>
    );
};

export default OnboardingDone;
