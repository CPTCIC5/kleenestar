import { FunctionComponent } from "react";
import FrameComponent2 from "../components/FrameComponent2";
import FrameComponent6 from "../components/FrameComponent6";

const JoinTeam: FunctionComponent = () => {
  return (
    <div className="w-full relative overflow-hidden flex flex-row items-end justify-start py-[0px] px-[113px] box-border gap-[69px] tracking-[normal] lg:flex-wrap mq750:gap-[69px_34px] mq750:pl-14 mq750:pr-14 mq750:box-border mq450:gap-[69px_17px] mq450:pl-5 mq450:pr-5 mq450:box-border">
      {/* <FrameComponent2
        decisionMakingProcess="decision-making process."
        frameDivWidth="129px"
        // frameDivDebugCommit="unset"
        frameDivWidth1="121px"
        alliahLaneMinWidth="unset"
        alliahLaneFlex="1"
        founderLayerioMinWidth="unset"
        founderLayerioAlignSelf="stretch"
        // groupIconDebugCommit="unset"
      /> */}
      <FrameComponent6 />
    </div>
  );
};

export default JoinTeam;
