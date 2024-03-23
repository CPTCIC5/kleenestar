import { FunctionComponent } from "react";
import FrameComponent8 from "./FrameComponent8";
import FrameComponent13 from "./FrameComponent13";
import FrameComponent7 from "./FrameComponent7";

const FrameComponent6: FunctionComponent = () => {
  return (
    <div className="flex-1 flex flex-col items-center justify-start pt-[85.40000000000009px] px-5 pb-[88.40000000000009px] box-border relative gap-[39px] min-w-[469px] max-w-full text-left text-sm text-darkslateblue-100 font-montserrat mq750:gap-[19px_39px] mq750:min-w-full mq450:pt-9 mq450:pb-[37px] mq450:box-border mq1050:pt-14 mq1050:pb-[57px] mq1050:box-border">
      <img
        className="w-full h-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full"
        alt=""
        src="/rectangle-506.svg"
      />
      <div className="w-[454px] flex flex-row items-start justify-center py-0 pr-0 pl-4 box-border max-w-full text-11xl font-syne">
        <div className="flex flex-col items-start justify-start gap-[19px]">
          <div className="flex flex-row items-start justify-start py-0 px-[53px] mq450:pl-5 mq450:pr-5 mq450:box-border">
            <h1 className="m-0 relative text-inherit font-bold font-inherit z-[1] mq750:text-5xl mq450:text-lg">
              Join Team
            </h1>
          </div>
          <div className="relative text-base font-montserrat z-[1]">
            Welcome to your team workspace 🙌
          </div>
        </div>
      </div>
      <div className="w-[454px] flex flex-col items-start justify-start gap-[10.900000000000093px] max-w-full">
        <FrameComponent8 unauthorizedEmail="Unauthorized email" />
        <FrameComponent13
          newPassword="Password*"
          password="Password"
          component627="/component-62--5.svg"
          propPadding="0px 0px 5.099999999999909px"
          propMinWidth="75px"
          propMinWidth1="73px"
        />
        <FrameComponent13
          newPassword="Confirm Password*"
          password="Confirm Password"
          component627="/component-62--1.svg"
          propPadding="unset"
          propMinWidth="unset"
          propMinWidth1="unset"
        />
        <div className="relative text-smi font-light text-orangered-300 z-[1]">
          Password doesn’t match
        </div>
      </div>
      <div className="w-[454px] flex flex-col items-end justify-start pt-0 px-0 pb-[7.199999999999818px] box-border gap-[25.300000000000185px] max-w-full text-mini">
        <button className="cursor-pointer [border:none] p-0 bg-[transparent] self-stretch h-10 relative">
          <img
            className="absolute top-[0px] left-[0px] w-[454px] h-10 z-[1]"
            alt=""
            src="/rectangle-512.svg"
          />
          <div className="absolute top-[10px] left-[197.4px] text-mini font-semibold font-montserrat text-whitesmoke text-left inline-block min-w-[60px] whitespace-nowrap z-[2]">
            Sign up
          </div>
        </button>
        <div className="self-stretch h-[25.5px] flex flex-row items-start justify-center py-0 px-5 box-border">
          <FrameComponent7 />
        </div>
      </div>
      <div className="w-[454px] flex flex-row items-start justify-center py-0 pr-0 pl-[9px] box-border max-w-full">
        <div className="relative z-[1]">
          {`Need a workspace? `}
          <span className="[text-decoration:underline]">
            Create a workspace
          </span>
        </div>
      </div>
    </div>
  );
};

export default FrameComponent6;
