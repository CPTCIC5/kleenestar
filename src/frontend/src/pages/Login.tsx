import { FunctionComponent } from "react";
import FrameComponent from "../components/FrameComponent";

const Login: FunctionComponent = () => {
  return (
    <div className="w-full relative bg-whitesmoke overflow-hidden flex flex-row items-end justify-start py-[99px] px-[113px] box-border gap-[67px] tracking-[normal] text-left text-xl text-darkslateblue-100 font-montserrat lg:flex-wrap mq750:gap-[67px_33px] mq750:pl-14 mq750:pr-14 mq750:box-border mq450:gap-[67px_17px] mq450:pl-5 mq450:pr-5 mq450:box-border">
      <div className="w-[495px] flex flex-col items-start justify-start min-w-[495px] min-h-[734px] max-w-full lg:flex-1 lg:min-h-[auto] mq750:min-w-full">
        <div className="self-stretch overflow-hidden flex flex-col items-start justify-end pt-0 px-0 pb-[4.547473508864641e-13px] gap-[35px] mq750:gap-[17px_35px]">
          <img
            className="self-stretch h-[436px] relative max-w-full overflow-hidden shrink-0 object-cover"
            loading="lazy"
            alt=""
            src="/infographic-1@2x.png"
          />
          <div className="self-stretch flex flex-col items-center justify-start pt-0 px-0 pb-[0.8000000000001819px] gap-[38px] shrink-0 mq750:gap-[19px_38px]">
            <i className="self-stretch relative font-semibold shrink-0 mq450:text-base">
              <p className="[margin-block-start:0] [margin-block-end:10px]">
                KleeneStar.io revolutionized our advertising
              </p>
              <p className="[margin-block-start:0] [margin-block-end:10px]">
                approach. Its intuitive, real-time insights help
              </p>
              <p className="[margin-block-start:0] [margin-block-end:10px]">
                us understand our KPI and transform our
              </p>
              <p className="m-0 whitespace-pre-wrap">{`decision-making process.  `}</p>
            </i>
            <div className="self-stretch flex flex-row items-center justify-between gap-[20px] shrink-0 text-lg mq450:flex-wrap">
              <div className="h-[49px] flex flex-col items-center justify-start gap-[9px]">
                <div className="flex-1 overflow-hidden flex flex-row items-center justify-start py-0 px-1 gap-[6px]">
                  <img
                    className="h-0.5 w-3 relative"
                    loading="lazy"
                    alt=""
                    src="/rectangle-510.svg"
                  />
                  <div className="relative font-semibold inline-block min-w-[103px]">
                    Alliah Lane
                  </div>
                </div>
                <div className="relative text-mini inline-block min-w-[129px]">
                  Founder, Layer.io
                </div>
              </div>
              <img
                className="h-[17.5px] w-[123.8px] relative"
                loading="lazy"
                alt=""
                src="/group-208.svg"
              />
            </div>
          </div>
        </div>
      </div>
      <FrameComponent />
    </div>
  );
};

export default Login;
