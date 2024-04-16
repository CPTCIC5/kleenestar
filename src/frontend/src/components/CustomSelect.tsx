import { Select } from "@radix-ui/themes";
import { Controller, Control, FieldValues } from "react-hook-form";

interface Option {
    value: string;
    label: string;
}

interface CustomSelectProps {
    name: string;
    control: Control<FieldValues>;
    placeholder?: string;
    options: Option[];
}

const CustomSelect: React.FC<CustomSelectProps> = ({ name, control, options, placeholder }) => {
    return (
        <Controller
            name={name}
            control={control}
            render={({ field }) => (
                <Select.Root size="3" onValueChange={field.onChange} value={field.value}>
                    <Select.Trigger
                        variant="soft"
                        placeholder={placeholder}
                        className="bg-background rounded-full w-full h-full  font-montserrat font-[400] text-[15px] leading-[18.29px] text-primary-300  text-opacity-50 outline-none"
                    />
                    <Select.Content position="popper" className="bg-background">
                        {options.map((option) => (
                            <Select.Item
                                key={option.value}
                                value={option.value}
                                onChange={field.onChange}
                                onBlur={field.onBlur}
                            >
                                {option.label}
                            </Select.Item>
                        ))}
                    </Select.Content>
                </Select.Root>
            )}
        />
    );
};

export default CustomSelect;
