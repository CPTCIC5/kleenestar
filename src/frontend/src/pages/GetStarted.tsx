import { FunctionComponent } from "react";

const GetStarted: FunctionComponent = () => {
    return (
        <div className="w-full h-screen flex items-center justify-center bg-background p-4">
            <div className="max-w-[722px] max-h-[684px] w-full h-full flex flex-col items-center justify-center rounded-3xl p-4">
                <div className="max-width flex items-center justify-center box-border max-w-full text-11xl font-syne">
                    <div className="flex-1 flex flex-col items-center justify-center gap-[19px] max-w-full">
                        <span className=" m-0 text-inherit font-bold font-inherit inline-block z-[1]">
                            Get Started
                        </span>
                        <div className="max-width self-stretch text-base text-center font-montserrat z-[1] flex flex-col items-center">
                            <span>A new way to run highly efficient marketing analytics </span>
                            <span>across channels and learn real-time insights 🚀</span>
                        </div>
                    </div>
                </div>

                <button className="cursor-pointer bg-primary-300 text-white rounded-full w-full h-[40px] shrink-0 border-none p-0 self-stretch position-relative max-w-[454px] mx-auto font-montserrat font-[600] text-[15px] leading-[18.29px] text-center mt-[39px] flex items-center justify-center gap-[10px]">
                    <span className="bg-primary-300 text-white">
                        Create a workspace
                    </span>
                    <svg
                        className="bg-inherit"
                        width="18"
                        height="15"
                        viewBox="0 0 18 15"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            opacity="0.5"
                            d="M0.875 6.75C0.676088 6.75 0.485322 6.82902 0.34467 6.96967C0.204018 7.11032 0.125 7.30109 0.125 7.5C0.125 7.69891 0.204018 7.88968 0.34467 8.03033C0.485322 8.17098 0.676088 8.25 0.875 8.25V6.75ZM0.875 8.25H16.875V6.75H0.875V8.25Z"
                            fill="white"
                        />
                        <path
                            d="M10.875 1.5L16.875 7.5L10.875 13.5"
                            stroke="white"
                            stroke-width="1.5"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        />
                    </svg>
                </button>

                <div className="h-[17px] w-full flex justify-center mt-[46.26px]">
                    <span className="h-[17px] font-montserrat text-[14px] font-[400] leading-[17.07px] text-center">
                        Already using KleeneStar?
                        <span className="underline">Log in to an existing workspace</span>
                    </span>
                </div>
            </div>
        </div>
    );
};

export default GetStarted;
