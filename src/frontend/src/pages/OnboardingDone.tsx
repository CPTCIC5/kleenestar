import { FunctionComponent } from "react";
import FrameComponent2 from "../components/FrameComponent2";
import FrameComponent51 from "../components/FrameComponent5";

const OnboardingDone: FunctionComponent = () => {
  return (
    <div className="w-full relative bg-whitesmoke overflow-hidden flex flex-row items-end justify-start py-[99px] px-[113px] box-border gap-[68px] tracking-[normal] lg:flex-wrap mq750:gap-[68px_34px] mq750:pl-14 mq750:pr-14 mq750:box-border mq450:gap-[68px_17px] mq450:pl-5 mq450:pr-5 mq450:box-border">
      <FrameComponent2
        decisionMakingProcess="decision-making process."
        frameDivWidth="unset"
        frameDivWidth1="unset"
        alliahLaneMinWidth="103px"
        alliahLaneFlex="unset"
        founderLayerioMinWidth="129px"
        founderLayerioAlignSelf="unset"
      />
      <FrameComponent51 />

    </div>
  );
};

export default OnboardingDone;
