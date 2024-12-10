import { View, Text } from "react-native";
import { TouchableOpacity } from "react-native";
import { useState } from "react";

export default function Index() {
  const [isPressed, setIsPressed] = useState<boolean>(false);

  return (
    <View className="flex-1 items-center justify-center">
      <TouchableOpacity onPress={() => setIsPressed(!isPressed)}>
        <Text
          className={`font-bold ${
            isPressed ? "text-[#8389ff]" : "text-[#001e57]"
          } ${isPressed ? "text-4xl" : "text-2xl"}`}
        >
          {isPressed ? "GOOD LUCK!" : "NECK IMAGE PROJECT"}
        </Text>
      </TouchableOpacity>
    </View>
  );
}
