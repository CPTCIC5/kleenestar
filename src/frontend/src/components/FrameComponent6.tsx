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
        <div className="relative font-medium inline-block min-w-[64px] shrink-0 [debug_commit:f6aba90]">
          Email
        </div>
        <div className="self-stretch flex flex-row items-start justify-start pt-[13.200000000000273px] px-[18.199999999999815px] pb-[13.799999999999727px] relative shrink-0 [debug_commit:f6aba90] text-mini text-darkslateblue-200">
          {/* <div className="relative inline-block min-w-[53px] z-[1]">
                  https://
                </div> */}
          <div className="relative inline-block min-w-[115px] z-[1] ">
            <input
              type="text"
              placeholder="@work-email.com"
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
              className="absolute top-[50%] transform -translate-y-1/2 right-2 w-4 h-auto z-[2]"
              alt=""
              src="/pen2svgrepocom1.svg"
            />
          </div>
        </div>
      </div>
      <div className="w-[454px] flex flex-col items-start justify-start gap-[10.900000000000093px] max-w-full">
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
      </div>
      <div className="w-[454px] flex flex-col items-start justify-start gap-[10.900000000000093px] max-w-full">
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
      <div className="w-[454px] flex flex-col items-end justify-start pt-0 px-0 pb-[7.199999999999818px] box-border gap-[25.300000000000185px] max-w-full text-mini">
      <button
            className="cursor-pointer"
            style={{
              backgroundColor: "#1C274C",
              color: "white",
              borderRadius: "10px",
              width: "100%", // Set width to 100% for responsiveness
              height: "40px",
              flexShrink: 0,
              border: "none", // If you want to remove the border
              padding: 0, // If you want to remove padding
              alignSelf: "stretch", // If you want the button to stretch vertically
              position: "relative", // If you want to position child elements absolutely
              maxWidth: "454px", // Set maximum width for larger screens
              margin: "0 auto", // Center the button horizontally
            }}
          >
            Signup
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
