import { FunctionComponent } from "react";
import FrameComponent8 from "./FrameComponent8";

const FrameComponent10: FunctionComponent = () => {
  return (
    <div className="w-[722px] flex flex-col items-center justify-start pt-[85px] px-5 pb-[88px] box-border relative gap-[39px] max-w-full text-left text-11xl text-darkslateblue-100 font-syne mq675:gap-[19px_39px] mq675:pt-[55px] mq675:pb-[57px] mq675:box-border">
      <img
        className="w-full h-full absolute !m-[0] top-[0px] right-[0px] bottom-[0px] left-[0px] max-w-full overflow-hidden max-h-full"
        alt=""
        src="/rectangle-506.svg"
      />
      <div className="w-[454px] flex flex-row items-start justify-end py-0 pr-[25px] pl-[26px] box-border max-w-full">
        <div className="flex-1 flex flex-col items-start justify-start gap-[14px] max-w-full">
          <div className="flex flex-row items-start justify-start py-0 pr-[73px] pl-[72px] mq450:pl-5 mq450:pr-5 mq450:box-border">
            <h1 className="m-0 relative text-inherit font-bold font-inherit z-[1] mq450:text-lg mq750:text-5xl">
              Recovery Email
            </h1>
          </div>
          <div className="self-stretch flex flex-col items-end justify-start gap-[4px] text-center text-base font-montserrat">
            <div className="self-stretch relative z-[1]">{`Send a password recovery email to your registered `}</div>
            <div className="self-stretch flex flex-row items-start justify-center py-0 pr-5 pl-[27px]">
              <div className="w-[136px] relative inline-block z-[1]">
                email address. 💁
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* <FrameComponent8
        unauthorizedEmail="Email not recognized"
        propAlignSelf="unset"
        propPadding="unset"
        propWidth="454px"
        propMinWidth="unset"
      /> */}
      <div
      className="self-stretch flex flex-col items-start justify-start pt-0 px-0 pb-[5.099999999999909px] gap-[10.799999999999956px] text-left text-sm text-darkslateblue-100 font-montserrat"
      // style={frameDiv3Style}
    >
      <div className="relative font-medium inline-block min-w-[46px] z-[1]">
        Email*
      </div>
      <div className="self-stretch flex flex-row items-start justify-start pt-[13.200000000000273px] px-[18.199999999999815px] pb-[13.799999999999727px] relative text-mini text-darkslateblue-200">
        {/* <div className="relative z-[2]">@work-email.com</div> */}
        <div className="h-full w-full   top-[0px] right-[0px] bottom-[0px] left-[0px]">
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
      <div className="w-[454px] flex flex-col items-end justify-start gap-[30px] max-w-full text-center text-sm font-montserrat">
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
            Continue
          </button><div className="relative inline-block min-w-[115px] z-[1] beautify">
  
</div>

        <div className="self-stretch flex flex-row items-start justify-center py-0 pr-5 pl-[21px]">
          <div className="w-[241px] relative inline-block z-[1]">
            {`Did not receive a code? `}
            <span className="[text-decoration:underline]">Send code</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FrameComponent10;
