import {
  View,
  Text,
  Image,
  ScrollView,
  Dimensions,
  ActivityIndicator,
  TouchableOpacity,
  Modal,
  Pressable,
} from "react-native";
import React, { useState } from "react";
import { useLocalSearchParams, router } from "expo-router";
import { useQuery } from "@tanstack/react-query";

interface Params {
  plotUrl: string;
  registrationData: string;
}

export default function Insight() {
  const screenWidth = Dimensions.get("window").width;
  const screenHeight = Dimensions.get("window").height;
  const containerWidth = screenWidth * 0.85;
  const params = useLocalSearchParams();
  const [modalVisible, setModalVisible] = useState(false);

  // VIC
  const SERVER_URL = "http://192.168.1.19:8000";
  // ABI
  // const SERVER_URL = "http://172.23.23.251:8000";

  const plotUrl = params.plotUrl;
  const registrationData = params.registrationData;

  const { data, isLoading } = useQuery({
    queryKey: ["plot", plotUrl],
    queryFn: async () => {
      const timestamp = Date.now();
      return `${SERVER_URL}${plotUrl}?t=${timestamp}`;
    },
    enabled: plotUrl !== undefined,
  });

  const handleNavigateToImaging = () => {
    router.push("/(tabs)/imaging");
  };

  return (
    <ScrollView contentContainerStyle={{ flex: 1 }}>
      <View
        className="flex-1 bg-gray-100 justify-center items-center"
        style={{ padding: screenWidth * 0.08 }}
      >
        <View
          className="bg-white rounded-xl"
          style={{
            width: containerWidth,
            padding: screenWidth * 0.05,
            
          }}
        >
          <Text
            className="text-[#001e57] font-bold text-center mb-6"
            style={{ fontSize: screenWidth * 0.06, marginBottom: screenHeight * 0.04 }}
          >
            Diagnosis Results
          </Text>
          {isLoading ? (
            <View className="items-center justify-center p-8">
              <ActivityIndicator size="large" color="#001e57" />
              <Text
                className="text-gray-600 mt-4 text-center"
                style={{ fontSize: screenWidth * 0.04 }}
              >
                Loading diagnosis results...
              </Text>
            </View>
          ) : data ? (
            <View>
              <View className="bg-gray-50 rounded-lg mb-4">
                <Image
                  source={{ uri: data }}
                  style={{
                    width: "100%",
                    height: screenWidth * 0.6,
                  }}
                  resizeMode="contain"
                />
              </View>
              {registrationData && (
                <View className="mt-4">
                  <TouchableOpacity
                    onPress={() => setModalVisible(true)}
                    className="bg-[#001e57] rounded-lg shadow-lg"
                    style={{
                      padding: screenWidth * 0.04,
                      marginBottom: screenHeight * 0.02,
                    }}
                  >
                    <Text
                      className="text-white text-center font-semibold"
                      style={{
                        fontSize: screenWidth * 0.04,
                      }}
                    >
                      More Information
                    </Text>
                  </TouchableOpacity>
                  <Modal
                    animationType="slide"
                    transparent={true}
                    visible={modalVisible}
                    onRequestClose={() => setModalVisible(false)}
                  >
                    <View className="flex-1 justify-center items-center bg-black/50">
                      <View className="bg-white rounded-xl p-6 m-5 w-4/5">
                        <Text
                          className="text-gray-600 text-center mb-4"
                          style={{ fontSize: screenWidth * 0.035 }}
                        >
                          Detailed data has been exported to csv file
                        </Text>
                        <Pressable
                          className="bg-[#001e57] rounded-lg shadow-lg"
                          style={{
                            padding: screenWidth * 0.04,
                            marginTop: screenHeight * 0.02,
                          }}
                          onPress={() => setModalVisible(false)}
                        >
                          <Text
                            className="text-white text-center font-semibold"
                            style={{
                              fontSize: screenWidth * 0.04,
                            }}
                          >
                            Close
                          </Text>
                        </Pressable>
                      </View>
                    </View>
                  </Modal>
                </View>
              )}
            </View>
          ) : (
            <TouchableOpacity
              onPress={handleNavigateToImaging}
              className="bg-[#001e57] rounded-lg shadow-lg"
              style={{
                padding: screenWidth * 0.04, marginBottom: screenHeight * 0.02
              }}
            >
              <Text
                className="text-white text-center font-semibold"
                style={{
                  fontSize: screenWidth * 0.04,
                }}
              >
                Run the diagnosis first
              </Text>
            </TouchableOpacity>
          )}
        </View>
      </View>
    </ScrollView>
  );
}
