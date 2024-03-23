import { FunctionComponent } from "react";
import FrameComponent1 from "./FrameComponent1";

const FrameComponent: FunctionComponent = () => {
  return (
    <div className="flex-1 flex flex-col items-center justify-start pt-[143.80000000000018px] px-5 pb-[145.5999999999999px] box-border relative gap-[39px] min-w-[469px] max-w-full text-center text-sm text-darkslateblue-100 font-montserrat mq750:gap-[19px_39px] mq750:min-w-full mq450:pt-[60px] mq450:pb-[62px] mq450:box-border mq1050:pt-[93px] mq1050:pb-[95px] mq1050:box-border">
      <img
        className="w-full h-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full"
        alt=""
        src="/rectangle-506.svg"
      />
      <div className="w-[454px] flex flex-row items-start justify-start py-0 pr-14 pl-[55px] box-border max-w-full text-11xl font-syne mq450:pl-[27px] mq450:pr-7 mq450:box-border">
        <div className="flex-1 flex flex-col items-start justify-start gap-[19px] max-w-full">
          <div className="flex flex-row items-start justify-start py-0 px-[45px] mq450:pl-5 mq450:pr-5 mq450:box-border">
            <h1 className="m-0 w-[253px] relative text-inherit font-bold font-inherit inline-block z-[1] mq750:text-5xl mq450:text-lg">
              Welcome back
            </h1>
          </div>
          <div className="self-stretch relative text-base font-montserrat z-[1]">
            Welcome back, log in to your workspace 🙌
          </div>
        </div>
      </div>
      <div className="w-[454px] flex flex-col items-start justify-start pt-0 px-0 pb-[7.200000000000273px] box-border gap-[40.30000000000018px] max-w-full text-left mq450:gap-[20px_40.3px]">
        <div className="self-stretch flex flex-col items-start justify-start gap-[10px]">
          <div className="self-stretch flex flex-col items-start justify-start pt-0 px-0 pb-[6.299999999999727px] gap-[10px]">
            <div className="relative font-medium inline-block min-w-[46px] z-[1]">
              Email*
            </div>
            <div className="self-stretch flex flex-row items-start justify-start pt-[13.199999999999818px] px-[18.199999999999815px] pb-[13.800000000000182px] relative text-mini text-darkslateblue-200">
              <div className="relative z-[2]">@work-email.com</div>
              <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
                <img
                  className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full z-[1]"
                  alt=""
                  src="/rectangle-522.svg"
                />
                <img
                  className="absolute top-[12.9px] left-[420.7px] w-[16.1px] h-[20.1px] z-[2]"
                  alt=""
                  src="/pen2svgrepocom.svg"
                />
              </div>
            </div>
          </div>
          <div className="self-stretch flex flex-col items-start justify-start gap-[10px]">
            <div className="relative font-medium inline-block min-w-[75px] z-[1]">
              Password*
            </div>
            <div className="self-stretch flex flex-row items-start justify-start pt-[13.200000000000273px] px-[18.199999999999815px] pb-[13.799999999999727px] relative text-mini text-darkslateblue-200">
              <div className="relative inline-block min-w-[73px] z-[2]">
                Password
              </div>
              <div className="h-full w-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px]">
                <img
                  className="absolute h-full w-full top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full z-[1]"
                  alt=""
                  src="/rectangle-522.svg"
                />
                <img
                  className="absolute top-[14.5px] left-[416.3px] w-[21.5px] h-[19px] z-[2]"
                  loading="lazy"
                  alt=""
                  src="/component-62--1.svg"
                />
              </div>
            </div>
          </div>
          <div className="self-stretch flex flex-row items-start justify-between gap-[20px] text-smi text-orangered-300 mq450:flex-wrap">
            <div className="relative font-light inline-block min-w-[123px] z-[1]">
              Password incorrect
            </div>
            <div className="relative [text-decoration:underline] font-light text-slategray inline-block min-w-[116px] z-[1]">
              Forgot password?
            </div>
          </div>
        </div>
        <div className="self-stretch flex flex-col items-start justify-start gap-[25.299999999999727px] text-mini">
          <button className="cursor-pointer [border:none] p-0 bg-[transparent] self-stretch h-10 relative">
            <img
              className="absolute top-[0px] left-[0px] w-[454px] h-10 z-[1]"
              alt=""
              src="/rectangle-512.svg"
            />
            <div className="absolute top-[10px] left-[203.2px] text-mini font-semibold font-montserrat text-whitesmoke text-center inline-block min-w-[44px] z-[2]">
              Login
            </div>
          </button>
          <div className="self-stretch h-[25.5px] flex flex-row items-start justify-center py-0 px-5 box-border">
            <FrameComponent1 />
          </div>
        </div>
      </div>
      <div className="w-[454px] flex flex-row items-start justify-center py-0 pr-px pl-0 box-border max-w-full">
        <div className="w-[277px] relative inline-block z-[1]">
          {`Need a workspace? `}
          <span className="[text-decoration:underline]">
            Create a workspace
          </span>
        </div>
      </div>
    </div>
  );
};

export default FrameComponent;
