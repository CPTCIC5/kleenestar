import * as React from "react";
import { Theme, useTheme } from "@mui/material/styles";
import Input from "@mui/material/Input";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import InputLabel from "@mui/material/InputLabel";

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250
    }
  }
};

function getStyles(
  name: string,
  personName: string[],
  theme: Theme
) {
  return {
    fontWeight:
      personName.indexOf(name) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium
  };
}

function SelectOptions({ options, InputText }: { options: Array<string>, InputText: string }) {
  const names = options;
  const theme = useTheme();
  const [personName, setPersonName] = React.useState<string>("");

  const handleChange = (
    event: SelectChangeEvent<typeof personName>
  ) => {
    const {
      target: { value }
    } = event;
    setPersonName(value);
  };

  return (
		<div className="w-full">
			<FormControl className="w-full">
				{!personName && (
					<InputLabel
						shrink={false}
						className="text-gray-500 focus:text-gray-500  px-1 mq750: py-1 border-transparent font-montserrat text-xl mq750:text-[15px]">
						{InputText}
					</InputLabel>
				)}
				<Select
					labelId="demo-multiple-name-label"
					id="demo-multiple-name"
					value={personName}
					onChange={handleChange}
					input={
						<Input
							disableUnderline
							className="w-full bg-transparent h-[45px] px-1 border-transparent font-montserrat text-xl mq750:text-[15px]"
						/>
					}
					IconComponent={() => null} // This line hides the dropdown arrow
					MenuProps={MenuProps}>
					{names.map((name) => (
						<MenuItem
							key={name}
							value={name}
							style={getStyles(name, [personName], theme)}>
							{name}
						</MenuItem>
					))}
				</Select>
			</FormControl>
		</div>
	)
}

export default SelectOptions;