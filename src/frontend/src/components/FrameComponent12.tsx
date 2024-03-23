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
        <div className="relative font-medium inline-block min-w-[75px] z-[1]">
          Password*
        </div>
        <div className="self-stretch flex flex-row items-start justify-start pt-[13.299999999999727px] px-[18.200000000000045px] pb-[13.700000000000273px] relative text-mini text-darkslateblue-200">
          <input
            type="text"
            placeholder="Password"
            className="border border-gray-300 outline-none px-2 py-1"
            style={{
              width: "454px",
              height: "45px",
              flexShrink: 0,
              fill: "#F8F9F7",
              borderRadius: "4px",
              border: "none",
            }}
          />
          <img
            className="absolute top-[13.5px] left-[418px] w-[21.5px] h-[19px] z-[2]"
            loading="lazy"
            alt=""
            src="/component-62--3.svg"
          />
        </div>
        <div className="relative font-medium inline-block min-w-[75px] z-[1]">
          Confirm Password*
        </div>
        <div className="self-stretch flex flex-row items-start justify-start pt-[13.299999999999727px] px-[18.200000000000045px] pb-[13.700000000000273px] relative text-mini text-darkslateblue-200">
          <input
            type="text"
            placeholder="Confirm Password"
            className="border border-gray-300 outline-none px-2 py-1"
            style={{
              width: "454px",
              height: "45px",
              flexShrink: 0,
              fill: "#F8F9F7",
              borderRadius: "4px",
              border: "none",
            }}
          />
          <img
            className="absolute top-[13.5px] left-[418px] w-[21.5px] h-[19px] z-[2]"
            loading="lazy"
            alt=""
            src="/component-62--3.svg"
          />
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
