import { FunctionComponent } from "react";
import FrameComponent2 from "../components/FrameComponent2";
import FrameComponent51 from "../components/FrameComponent5";

const OnboardingDone: FunctionComponent = () => {
    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4">
            <div className="max-w-[722px] max-h-[684px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4">
                <div className="max-width flex items-center justify-center box-border max-w-full text-11xl font-syne">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className=" m-0 text-inherit font-bold font-inherit inline-block z-[1]">
                            Welcome
                        </span>
                        <div className="max-width self-stretch text-base text-center font-montserrat z-[1] flex flex-col items-center">
                            <span>Congratulations you are all set 🤩 </span>
                            <span>Go to your workspace, connect your advertising </span>
                            <span>channels, and start learning.</span>
                        </div>
                    </div>
                </div>

                <div className="max-w-[454px] w-full my-2 mt-[40px]">
                    <img
                        src="/welcome-onboard-done-img.svg"
                        alt=""
                        className="max-w-full h-auto block m-auto "
                    />
                </div>

                <button className="cursor-pointer bg-primary-300 text-white rounded-full w-full h-[40px] shrink-0 border-none p-0 self-stretch position-relative max-w-[454px] mx-auto font-montserrat font-[600] text-[15px] leading-[18.29px] text-center mt-[39px] flex items-center justify-center gap-[10px]">
                    <span className="bg-primary-300 text-white">Get started</span>
                </button>
            </div>
        </div>
    );
};

export default OnboardingDone;
