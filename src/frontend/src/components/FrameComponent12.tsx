import { FunctionComponent } from "react";
import FrameComponent13 from "./FrameComponent13";

const FrameComponent12: FunctionComponent = () => {
  return (
    <div className="w-[722px] flex flex-col items-center justify-start pt-[85px] px-5 pb-[87px] box-border relative gap-[39px] max-w-full text-left text-11xl text-darkslateblue-100 font-syne mq675:gap-[19px_39px] mq675:pt-[55px] mq675:pb-[57px] mq675:box-border">
      <img
        className="w-full h-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full"
        alt=""
        src="/rectangle-506.svg"
      />
      <div className="w-[454px] flex flex-row items-start justify-end py-0 pr-[41px] pl-[42px] box-border max-w-full mq450:pl-[21px] mq450:box-border">
        <div className="flex-1 flex flex-col items-start justify-start gap-[19px] max-w-full">
          <div className="self-stretch flex flex-row items-start justify-center py-0 px-5">
            <h1 className="m-0 relative text-inherit font-bold font-inherit z-[1] mq450:text-lg mq750:text-5xl">
              Password
            </h1>
          </div>
          <div className="self-stretch relative text-base font-montserrat text-center z-[1]">
            Reset your password by creating a new one. 🥸
          </div>
        </div>
      </div>
      <div className="w-[454px] flex flex-col items-start justify-start gap-[10.900000000000093px] max-w-full text-sm font-montserrat">
        <FrameComponent13
          newPassword="New Password*"
          password="Password"
          component627="/component-62--5.svg"
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
      <button className="cursor-pointer [border:none] p-0 bg-[transparent] w-[454px] h-10 relative max-w-full">
        <img
          className="absolute top-[0px] left-[0px] w-[454px] h-10 z-[1]"
          alt=""
          src="/rectangle-512.svg"
        />
        <div className="absolute top-[10px] left-[169.7px] text-mini font-semibold font-montserrat text-whitesmoke text-left inline-block min-w-[115px] z-[2]">
          Save password
        </div>
      </button>
    </div>
  );
};

export default FrameComponent12;
