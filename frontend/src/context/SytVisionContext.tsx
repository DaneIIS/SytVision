import { QueryKey, useQueryClient } from "@tanstack/react-query";
import React, { FC, createContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuthContext } from "context/AuthContext";
import { toastIds, useToast } from "hooks/UseToast";
import { Connection, SubscriptionUnsubscribe } from "lib/websockets";

/** Provider props */
export type SytVisionProviderProps = {
  children: React.ReactNode;
};

type SubscriptionManager = {
  count: number;
  unsubscribe: SubscriptionUnsubscribe | null;
  subscribing: boolean;
  queryKeys: QueryKey[];
};

/** Context state */
export type SytVisionContextState = {
  connection: Connection | undefined;
  connected: boolean;
  safeMode: boolean;
  version: string | undefined;
  gitCommit: string | undefined;
  subscriptionRef:
    | React.MutableRefObject<Record<string, SubscriptionManager>>
    | undefined;
};

/** Defaults */
const contextDefaultValues: SytVisionContextState = {
  connection: undefined,
  connected: false,
  safeMode: false,
  version: undefined,
  gitCommit: undefined,
  subscriptionRef: undefined,
};

/** The Context (exported) */
export const SytVisionContext = createContext<SytVisionContextState>(
  contextDefaultValues
);

/** The Provider (exported) */
export const SytVisionProvider: FC<SytVisionProviderProps> = ({ children }) => {
  const { auth } = useAuthContext();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const toast = useToast();

  const subscriptionRef = React.useRef<Record<string, SubscriptionManager>>({});
  const [contextValue, setContextValue] = useState<SytVisionContextState>({
    ...contextDefaultValues,
    subscriptionRef,
  });

  const { connection } = contextValue;

  const onConnectRef = React.useRef<() => void>();
  const onDisconnectRef = React.useRef<() => void>();
  const onConnectionErrorRef = React.useRef<() => void>();

  useEffect(() => {
    if (connection) {
      onConnectRef.current = async () => {
        // invalidate all queries on connect
        queryClient.invalidateQueries();
        setContextValue((prev) => ({
          ...prev,
          connected: true,
          safeMode: !!connection.system_information?.safe_mode,
          version: connection.system_information?.version,
          gitCommit: connection.system_information?.git_commit,
        }));
      };

      onDisconnectRef.current = async () => {
        setContextValue((prev) => ({
          ...prev,
          connected: false,
        }));
      };

      onConnectionErrorRef.current = async () => {
        if (auth.enabled) {
          const url = auth.onboarding_complete ? "/login" : "/onboarding";
          // eslint-disable-next-line no-console
          console.error(`Connection error, redirecting to ${url}`);
          navigate(url);
        }
      };

      connection.addEventListener("connected", onConnectRef.current);
      connection.addEventListener("disconnected", onDisconnectRef.current);
      connection.addEventListener("connection-error", onConnectionErrorRef.current);

      const connect = async () => {
        await connection.connect();
      };
      connect();
    }

    return () => {
      if (connection) {
        if (onConnectRef.current) {
          connection.removeEventListener("connected", onConnectRef.current);
        }
        if (onDisconnectRef.current) {
          connection.removeEventListener("disconnected", onDisconnectRef.current);
        }
        if (onConnectionErrorRef.current) {
          connection.removeEventListener("connection-error", onConnectionErrorRef.current);
        }

        connection.disconnect();

        setContextValue((prev) => ({
          ...prev,
          connection: undefined,
        }));

        toast.dismiss(toastIds.websocketConnecting);
        toast.dismiss(toastIds.websocketConnectionLost);
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [connection, queryClient]);

  useEffect(() => {
    setContextValue((prev) => ({
      ...prev,
      connection: new Connection(toast),
    }));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <SytVisionContext.Provider value={contextValue}>
      {children}
    </SytVisionContext.Provider>
  );
};
