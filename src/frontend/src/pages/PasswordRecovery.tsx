import { FunctionComponent } from "react";
import FrameComponent12 from "../components/FrameComponent12";

const PasswordRecovery: FunctionComponent = () => {
  return (
    <div className="w-full relative overflow-hidden flex flex-col items-center justify-start pt-[30px] px-5 pb-[0.4000000000001px] box-border gap-[91.69999999999982px] tracking-[normal] text-left text-6xl text-darkslateblue-100 font-syne mq450:gap-[23px_91.7px] mq750:gap-[46px_91.7px]">
      <div className="w-[722px] h-[52.3px] flex flex-row items-start justify-center max-w-full">
        <div className="self-stretch flex flex-row items-start justify-start gap-[17.800000000000182px]">
          <img
            className="h-[52.3px] w-[49.7px] relative shrink-0 [debug_commit:f6aba90]"
            loading="lazy"
            alt=""
            src="/group-672.svg"
          />
          <div className="flex flex-col items-start justify-start pt-[11px] px-0 pb-0">
            <h2 className="m-0 relative text-inherit font-bold font-inherit shrink-0 [debug_commit:f6aba90] mq450:text-xl">
              Kleenestar
            </h2>
          </div>
        </div>
      </div>
      <FrameComponent12 />
    </div>
  );
};

export default PasswordRecovery;
