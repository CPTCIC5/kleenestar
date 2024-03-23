import { FunctionComponent } from "react";
import FrameComponent3 from "../components/FrameComponent3";
import BusinessNameContainer from "../components/BusinessNameContainer";

const OnboardingStep: FunctionComponent = () => {
  return (
    <div className="w-full relative bg-whitesmoke overflow-hidden flex flex-row items-end justify-start py-[99px] pr-[113px] pl-[114px] box-border gap-[68px] tracking-[normal] lg:flex-wrap mq750:gap-[68px_34px] mq750:pl-[57px] mq750:pr-14 mq750:box-border mq450:gap-[68px_17px] mq450:pl-5 mq450:pr-5 mq450:box-border">
      <FrameComponent3 />
      <BusinessNameContainer />
    </div>
  );
};

export default OnboardingStep;
