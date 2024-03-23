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
      <FrameComponent8
        unauthorizedEmail="Email not recognized"
        propAlignSelf="unset"
        propPadding="unset"
        propWidth="454px"
        propMinWidth="unset"
      />
      <div className="w-[454px] flex flex-col items-end justify-start gap-[30px] max-w-full text-center text-sm font-montserrat">
        <button className="cursor-pointer [border:none] p-0 bg-[transparent] self-stretch h-10 relative">
          <img
            className="absolute top-[0px] left-[0px] w-[454px] h-10 z-[1]"
            alt=""
            src="/rectangle-512.svg"
          />
          <div className="absolute top-[10px] left-[180.8px] text-mini font-semibold font-montserrat text-whitesmoke text-center inline-block min-w-[87px] z-[2]">
            Send email
          </div>
        </button>
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
